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

# If on master, ensure no agent-specific files are modified
if [ "$BRANCH" = "master" ]; then
  for f in $MODIFIED; do
    if [[ "$f" == $OPENCODE_DIR* || "$f" == $PIDEV_DIR* ]]; then
      echo "ERROR: Agent-specific file $f modified on master. Move to an agent branch or update policy." >&2
      exit 2
    fi
  done
  echo "Master validation passed."
  exit 0
fi

echo "Branch validation passed."
exit 0
