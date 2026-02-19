#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# POPDEUXREM // QUANTUM SURFACE AUTO-UPDATER
# Daily cron job for telemetry sync and README regeneration
# ═══════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "◈ Quantum Surface Updater v8.0"
echo "────────────────────────────────"

cd "$ROOT_DIR"

# Run telemetry fetcher if available
if [[ -f "scripts/discovery.py" ]]; then
    echo "▸ Fetching telemetry..."
    python3 scripts/discovery.py 2>/dev/null || true
fi

# Run vulnerability scanner if available
if [[ -f "scripts/vuln_scan.sh" ]]; then
    echo "▸ Running security scan..."
    bash scripts/vuln_scan.sh 2>/dev/null || true
fi

# Build README
if [[ -f "scripts/build_readme.py" ]]; then
    echo "▸ Building README..."
    python3 scripts/build_readme.py
fi

if git diff --quiet README.md 2>/dev/null; then
    echo "▸ No README changes detected"
else
    echo "▸ README updated, committing..."
    git add README.md assets/*.svg dist/*.svg
    git commit -m "sys: quantum surface v8 sync [skip ci]" 2>/dev/null || true
fi

echo "◈ Sync complete: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"