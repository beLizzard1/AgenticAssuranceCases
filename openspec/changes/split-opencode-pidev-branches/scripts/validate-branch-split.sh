#!/usr/bin/env bash
# Lightweight validation script to check modified files against branch-split policy
# Usage: scripts/validate-branch-split.sh <branch>

set -euo pipefail

BRANCH=${1:-$(git rev-parse --abbrev-ref HEAD)}

echo "Validating branch-split policy for branch: $BRANCH"

# Define agent directories
OPENCODE_DIR="agents/opencode/"
PIDEV_DIR="agents/pidev/"

# Get list of modified files in the current HEAD vs origin/master
git fetch origin master --quiet || true
MODIFIED=$(git diff --name-only origin/master...HEAD || true)

if [ -z "$MODIFIED" ]; then
  echo "No changes detected vs origin/master"
  exit 0
fi

echo "Modified files:\n$MODIFIED"

# If we're on a non-master branch, reject non-packaging changes
if [ "$BRANCH" != "master" ]; then
  for f in $MODIFIED; do
    # packaging files allowed in agent branches
    if [[ "$f" == agents/*/pi.yaml ]] || [[ "$f" == agents/*/package.yaml ]] || [[ "$f" == agents/*/Dockerfile ]] || [[ "$f" == agents/*/build/* ]] || [[ "$f" == agents/*/dist/* ]]; then
      continue
    fi
    # allow edits under agents/<agent>/README.md as non-normative docs
    if [[ "$f" == agents/*/README.md ]]; then
      continue
    fi
    # any other changes touching shared code/docs/skills are not allowed on agent branches
    if [[ "$f" == .opencode/skills/* ]] || [[ "$f" == docs/* ]] || [[ "$f" == README.md ]] || [[ "$f" == scripts/* ]] || [[ "$f" == mcp-server/* ]] || [[ "$f" == schemas/* ]] || [[ "$f" == .opencode/agents/* ]]; then
      echo "ERROR: Non-packaging file $f modified on branch '$BRANCH'. Non-packaging changes must be made on master and then propagated to branches." >&2
      exit 2
    fi
  done
  echo "Branch validation passed (packaging-only changes allowed)."
  exit 0
fi

# If on master, ensure packaging artifacts are not accidentally modified here? We allow packaging in master but prefer packaging in agent branches.
for f in $MODIFIED; do
  if [[ "$f" == agents/pidev/*/pi.yaml ]] || [[ "$f" == agents/pidev/pi.yaml ]] ; then
    echo "WARNING: Packaging metadata for pidev modified on master. Packaging is preferred to live in agent branches, but allowed."
  fi
done

echo "Master validation passed."
exit 0
