#!/usr/bin/env bash
set -euo pipefail

HEALTH_FILE="health/system_health.json"

if [[ ! -f "$HEALTH_FILE" ]]; then
  echo '{"status":"unknown","severity":"unknown"}'
  exit 0
fi

STATUS=$(jq -r '.status // "unknown"' "$HEALTH_FILE")
REPOS=$(jq -r '.repos_synced // 0' health/orchestrator.json 2>/dev/null || echo "0")

if [[ "$STATUS" == "healthy" ]]; then
  SEVERITY="low"
elif [[ "$STATUS" == "degraded" ]]; then
  SEVERITY="medium"
else
  SEVERITY="high"
fi

cat <<JSON
{
  "status": "$STATUS",
  "severity": "$SEVERITY",
  "repos_online": $REPOS
}
JSON
