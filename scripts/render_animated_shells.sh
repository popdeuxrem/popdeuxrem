#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[render] quantum-shell-infra.tape → quantum-shell-animated.gif"
vhs assets/terminal/quantum-shell-infra.tape

echo "[render] quantum-basilica-shell.tape → quantum-basilica-shell-animated.gif"
vhs assets/terminal/quantum-basilica-shell.tape

echo "[render] done."
