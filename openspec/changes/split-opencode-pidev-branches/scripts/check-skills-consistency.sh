#!/usr/bin/env bash
set -euo pipefail

echo "Checking skills consistency against master"

# Fetch master
git fetch origin master --quiet || true

# For each file under .opencode/skills, compare to master version
DIFF_FOUND=0
for f in $(git ls-files .opencode/skills || true); do
  if git show origin/master:$f >/dev/null 2>&1; then
    if ! git diff --no-index --quiet <(git show origin/master:$f) $f 2>/dev/null; then
      echo "DIFFERENCE: $f differs from master"
      DIFF_FOUND=1
    fi
  else
    echo "NEW: $f is new in this branch"
  fi
done

if [ "$DIFF_FOUND" -eq 1 ]; then
  echo "Skills consistency check failed: some .opencode/skills files differ from master. If this is intentional, include a rationale in agents.md."
  exit 2
fi

echo "Skills consistency check passed."
exit 0
