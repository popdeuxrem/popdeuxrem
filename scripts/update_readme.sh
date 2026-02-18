#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# POPDEUXREM // QUANTUM SURFACE AUTO-UPDATER
# Daily cron job for telemetry sync and README regeneration
# ═══════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "◈ Quantum Surface Updater v7.0"
echo "────────────────────────────────"

cd "$ROOT_DIR"

if [[ -f "scripts/build_readme.py" ]]; then
    echo "▸ Building README..."
    python3 scripts/build_readme.py --quiet 2>/dev/null || python scripts/build_readme.py
fi

if git diff --quiet README.md 2>/dev/null; then
    echo "▸ No README changes detected"
else
    echo "▸ README updated, committing..."
    git add README.md assets/*.svg dist/*.svg
    git commit -m "sys: quantum surface v7 sync [skip ci]" 2>/dev/null || true
fi

echo "◈ Sync complete: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"