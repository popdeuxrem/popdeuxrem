#!/usr/bin/env bash
set -euo pipefail

BASE="README.base.md"
OUT="README.md"

START="<!-- AUTO-GENERATED:START -->"
END="<!-- AUTO-GENERATED:END -->"

TMP="$(mktemp)"

# Generate dynamic block
DYNAMIC=$(cat <<BLOCK

$START

## ⚙️ System Telemetry

### System Health
\`\`\`json
$(cat health/system_health.json 2>/dev/null || echo '{}')
\`\`\`

### Orchestrator
\`\`\`json
$(cat health/orchestrator.json 2>/dev/null || echo '{}')
\`\`\`

### Aggregate Metrics
\`\`\`json
$(cat metrics/aggregate.json 2>/dev/null || echo '{}')
\`\`\`

$END

BLOCK
)

# If base missing, fail safe
if [[ ! -f "$BASE" ]]; then
  echo "[ERROR] README.base.md missing"
  exit 1
fi

# Inject or replace block
awk -v start="$START" -v end="$END" -v new="$DYNAMIC" '
BEGIN {found=0}
/start/ {print new; skip=1; found=1; next}
/end/ {skip=0; next}
!skip {print}
END {
  if (!found) {
    print "\n" new
  }
}
' "$BASE" > "$TMP"

mv "$TMP" "$OUT"

echo "[+] README updated (non-destructive)"
