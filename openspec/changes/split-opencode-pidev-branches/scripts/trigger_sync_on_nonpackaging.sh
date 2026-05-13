#!/usr/bin/env bash
set -euo pipefail

# Trigger a GitHub issue when a PR/commit contains non-packaging changes so maintainers
# can sync those changes to other branches. Optionally this script can be extended to
# create PRs automatically when configured with write tokens and gh cli.

REPO=${GITHUB_REPOSITORY:-}
if [ -z "$REPO" ]; then
  echo "GITHUB_REPOSITORY not set; skipping sync trigger"
  exit 0
fi

BASE_REF=${GITHUB_BASE_REF:-master}
HEAD_REF=${GITHUB_HEAD_REF:-}
EVENT_NAME=${GITHUB_EVENT_NAME:-}

echo "Trigger sync check: base=$BASE_REF head=$HEAD_REF event=$EVENT_NAME"

# Fetch base
git fetch origin "$BASE_REF" --quiet || true

if [ -n "$HEAD_REF" ]; then
  MODIFIED=$(git diff --name-only origin/$BASE_REF...HEAD || true)
else
  # fallback: compare against origin/master
  MODIFIED=$(git diff --name-only origin/$BASE_REF...HEAD || true)
fi

if [ -z "$MODIFIED" ]; then
  echo "No modified files detected"
  exit 0
fi

echo "Modified files:\n$MODIFIED"

# Packaging patterns: files under agents/pidev/ and pi.yaml
is_nonpack=0
for f in $MODIFIED; do
  if [[ "$f" == agents/pidev/* ]] || [[ "$(basename "$f")" == "pi.yaml" ]]; then
    echo "Packaging file: $f"
  else
    echo "Non-packaging file detected: $f"
    is_nonpack=1
  fi
done

if [ "$is_nonpack" -eq 0 ]; then
  echo "All changes are packaging-only; no sync required."
  exit 0
fi

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "GITHUB_TOKEN not available; cannot create issue. Please enable GITHUB_TOKEN in workflow."
  exit 0
fi

API_URL="https://api.github.com/repos/$REPO/issues"
TITLE="Branch sync required: non-packaging changes detected (${GITHUB_SHA:-unknown})"
BODY=$(cat <<EOF
Non-packaging changes were detected in this PR/commit and should be propagated to other branches (opencode and pidev).

Modified files:
$(printf '%s

Suggested actions:
1. Review the changes and apply the same modifications to the other branches (opencode, pidev) unless they are packaging-only.
2. Consider opening sync PRs from the branch containing the change to the other branches (e.g., create branch `sync/<target>/<short>` and cherry-pick or apply the patch).

If you'd like automatic PR creation, configure the repo CI with a write token and update the sync script to create PRs.

This issue was created automatically by branch-split validation.
EOF
)

echo "Creating issue on $API_URL"
curl -s -S -H "Authorization: Bearer $GITHUB_TOKEN" -H "Content-Type: application/json" -d "{\"title\": \"${TITLE}\", \"body\": \"${BODY//$'\n'/\\n}\", \"labels\": [\"branch-sync-needed\"]}" $API_URL

echo "Issue created (if API permitted)."
exit 0
