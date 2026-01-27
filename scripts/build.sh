#!/bin/bash
set -e

echo "◈ STARTING SPECTRE v5.0 REFINEMENT BUILD..."

# 1. Permission Fix
chmod +x scripts/*.py

# 2. Cleanup Legacy
if [ -f "scripts/cleanup.sh" ]; then
    bash scripts/cleanup.sh
fi

# 3. Design Engine & Hydration
python3 scripts/update_readme.py

echo "◈ SURFACE POLISHED. HIERARCHY ENFORCED."
