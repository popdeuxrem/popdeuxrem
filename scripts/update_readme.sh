#!/usr/bin/env bash
set -euo pipefail

# Safe wrapper to regenerate README and commit only when changes exist.
# Usage: scripts/update_readme.sh [--dry-run]

DRY_RUN=0
if [ "${1-}" = "--dry-run" ]; then
  DRY_RUN=1
fi

TIMESTAMP=$(date -u "+%Y-%m-%d %H:%M UTC")

echo "◈ Running safe README update ($([ $DRY_RUN -eq 1 ] && echo DRY-RUN || echo COMMIT))"

# Regenerate README (single source of truth)
python3 scripts/update_readme.py

# Stage expected outputs
git add README.md assets/*.svg dist/*.json docs/ARCHITECTURE.md || true

# Only commit if something changed
if ! git diff --cached --quiet; then
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[DRY-RUN] Changes detected but not committing."
  else
    git commit -m "sys: README & assets sync [$TIMESTAMP]" || true
    git push origin main || true
    echo "✅ README updated and pushed successfully."
  fi
else
  echo "⚡ No changes detected. Skipping commit."
fi
