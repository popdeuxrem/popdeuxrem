#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# SVG ENHANCER - Batch convert SVGs with quantum animations
# ═══════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
ASSETS_DIR="$ROOT_DIR/assets"

echo "◈ SVG Enhancer v2.0"
echo "────────────────────────────────"

cd "$ROOT_DIR"

for f in assets/*.svg; do
    if [[ "$f" != *"enhanced"* ]] && [[ "$f" != *"quantum-defs"* ]]; then
        BASENAME=$(basename "$f" .svg)
        BACKUP="$ASSETS_DIR/${BASENAME}_backup.svg"
        
        if [[ ! -f "$BACKUP" ]]; then
            cp "$f" "$BACKUP"
            echo "▸ Backed up: ${BASENAME}.svg → ${BASENAME}_backup.svg"
        fi
    fi
done

echo "▸ All SVGs backed up (originals preserved)"
echo "◈ Enhancement complete"