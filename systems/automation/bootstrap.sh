#!/usr/bin/env bash
set -euo pipefail

echo "[+] Bootstrapping system..."

mkdir -p logs metrics health

echo "$(date -Iseconds) BOOTSTRAP_OK" >> logs/system.log

echo "{
  \"status\": \"running\",
  \"timestamp\": \"$(date -Iseconds)\"
}" > health/status.json