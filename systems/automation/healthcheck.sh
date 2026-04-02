#!/usr/bin/env bash
set -euo pipefail

echo "[+] Running healthcheck..."

if [[ -f health/status.json ]]; then
  echo "[OK] Health file exists"
else
  echo "[FAIL] Missing health file"
  exit 1
fi