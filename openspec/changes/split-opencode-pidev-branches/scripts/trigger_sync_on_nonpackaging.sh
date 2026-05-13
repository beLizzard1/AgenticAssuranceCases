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
2. This CI may attempt to create sync PRs automatically (if GITHUB_TOKEN is provided and changes apply cleanly).

This issue was created automatically by branch-split validation.
EOF
)

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "GITHUB_TOKEN not available; creating issue only."
  curl -s -S -H "Authorization: Bearer $GITHUB_TOKEN" -H "Content-Type: application/json" -d "{\"title\": \"${TITLE}\", \"body\": \"${BODY//$'\n'/\\n}\", \"labels\": [\"branch-sync-needed\"]}" $API_URL || true
  echo "Done (no token for PR creation)."
  exit 0
fi

echo "Creating issue on $API_URL"
curl -s -S -H "Authorization: Bearer $GITHUB_TOKEN" -H "Content-Type: application/json" -d "{\"title\": \"${TITLE}\", \"body\": \"${BODY//$'\n'/\\n}\", \"labels\": [\"branch-sync-needed\"]}" $API_URL || true

echo "Attempting automatic sync PR creation"

# Create PRs to other agent branches where applicable
TARGET_BRANCHES=(opencode pidev)
SHORT_SHA=$(echo "${GITHUB_SHA:-$(git rev-parse --short HEAD)}")

ORIGIN_REMOTE="https://x-access-token:${GITHUB_TOKEN}@github.com/${REPO}.git"

PATCH_FILE=$(mktemp)
git diff origin/$BASE_REF...HEAD > "$PATCH_FILE"

for target in "${TARGET_BRANCHES[@]}"; do
  if [ "$target" = "$HEAD_REF" ] || [ "$target" = "${GITHUB_REF##*/}" ]; then
    echo "Skipping target $target (same as head)"
    continue
  fi

  echo "Preparing sync branch for target: $target"
  SYNC_BRANCH="sync/${target}/${SHORT_SHA}"

  # fetch target and create a new branch from it
  git fetch origin $target --quiet || { echo "Failed to fetch origin/$target"; continue; }
  git checkout -b "$SYNC_BRANCH" origin/$target || { echo "Failed to checkout origin/$target"; continue; }

  # try to apply patch
  if git apply --index "$PATCH_FILE" --3way; then
    git commit -m "chore(sync): apply non-packaging changes from ${HEAD_REF:-$GITHUB_REF} to ${target}" || true
    # push the sync branch
    if git push "$ORIGIN_REMOTE" HEAD:"$SYNC_BRANCH"; then
      # create PR
      PR_TITLE="chore(sync): sync non-packaging changes to $target"
      PR_BODY="This PR was created automatically to propagate non-packaging changes from ${HEAD_REF:-$GITHUB_REF} to ${target}. Please review."
      API_PR_URL="https://api.github.com/repos/$REPO/pulls"
      curl -s -S -H "Authorization: Bearer $GITHUB_TOKEN" -H "Content-Type: application/json" -d "{\"title\": \"${PR_TITLE}\", \"head\": \"${SYNC_BRANCH}\", \"base\": \"${target}\", \"body\": \"${PR_BODY}\"}" $API_PR_URL || true
      echo "Created PR for $target from $SYNC_BRANCH"
    else
      echo "Push failed for $SYNC_BRANCH; skipping PR creation"
    fi
  else
    echo "Patch could not be applied cleanly to $target; skipping automatic PR creation. Manual intervention required."
  fi

  # return to head ref
  git checkout - >/dev/null 2>&1 || true
done

rm -f "$PATCH_FILE"

echo "Done."
exit 0
