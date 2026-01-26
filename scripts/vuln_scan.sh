#!/bin/bash
# VULN_SCAN.sh v1.0.9 - Final JSON Integrity Patch
REPORT_DIR="dist"
ASSET_DIR="assets"
mkdir -p "$REPORT_DIR" "$ASSET_DIR"

echo "◈ INITIALIZING SECURITY AUDIT..."

VULN_COUNT_CRIT=0
VULN_COUNT_HIGH=0
VULN_COUNT_MED=0

# 1. Dependency Audit
if command -v pip-audit &> /dev/null; then
    VULN_COUNT_HIGH=$(pip-audit -r requirements.txt --format json 2>/dev/null | grep -c "description" || echo 0)
elif [ -f requirements.txt ]; then
    VULN_COUNT_MED=$(grep -cv "==" requirements.txt 2>/dev/null || echo 0)
fi

# 2. Secret Pattern Scan
echo "◈ Scanning for secret patterns..."
SECRETS_FOUND=$(grep -rE "AIza[a-zA-Z0-9_-]{35}|AKIA[A-Z0-9]{16}" . \
    --exclude-dir=".git" --exclude-dir="dist" --exclude-dir="assets" \
    --exclude="*.svg" --exclude="*.json" --exclude="vuln_scan.sh" 2>/dev/null | wc -l | xargs)

# 3. Executable Audit
EXEC_COUNT=$(find . -maxdepth 1 -type f -executable -not -path "*/.*" 2>/dev/null | wc -l | xargs)

# 4. Status Determination
HYGIENE_STATUS="PASS"
if [ "${SECRETS_FOUND:-0}" -gt 0 ] || [ "${EXEC_COUNT:-0}" -gt 0 ]; then
    HYGIENE_STATUS="WARN"
fi

# 5. JSON Generation (Explicitly verified trailing comma on line 7)
printf '{\n  "timestamp": "%s",\n  "vulnerabilities": {\n    "critical": %d,\n    "high": %d,\n    "medium": %d\n  },\n  "hygiene": "%s",\n  "engine_version": "QuantumSec/v1.0.9"\n}\n' \
    "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    "$VULN_COUNT_CRIT" \
    "$VULN_COUNT_HIGH" \
    "$VULN_COUNT_MED" \
    "$HYGIENE_STATUS" > "$REPORT_DIR/security-report.json"

echo "◈ Security report generated: $REPORT_DIR/security-report.json"
exit 0
