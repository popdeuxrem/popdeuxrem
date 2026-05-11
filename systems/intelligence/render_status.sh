#!/usr/bin/env bash
set -euo pipefail

HEALTH_FILE="health/system_health.json"
ORCHESTRATOR_FILE="health/orchestrator.json"

if [[ ! -f "$HEALTH_FILE" ]]; then
  cat <<JSON
{
  "status": "unknown",
  "severity": "unknown",
  "repos_online": 0
}
JSON
  exit 0
fi

if command -v jq >/dev/null 2>&1; then
  STATUS="$(jq -r '.status // "unknown"' "$HEALTH_FILE")"
  REPOS="$(jq -r '.repos_synced // 0' "$ORCHESTRATOR_FILE" 2>/dev/null || echo "0")"
else
  STATUS="$(python3 - "$HEALTH_FILE" << 'PY'
import json, sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    print(json.load(f).get("status", "unknown"))
PY
)"
  REPOS="$(python3 - "$ORCHESTRATOR_FILE" << 'PY' 2>/dev/null || echo "0"
import json, sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    print(json.load(f).get("repos_synced", 0))
PY
)"
fi

case "$STATUS" in
  healthy)
    SEVERITY="low"
    ;;
  watch)
    SEVERITY="medium"
    ;;
  degraded)
    SEVERITY="high"
    ;;
  *)
    SEVERITY="unknown"
    ;;
esac

cat <<JSON
{
  "status": "$STATUS",
  "severity": "$SEVERITY",
  "repos_online": $REPOS
}
JSON
