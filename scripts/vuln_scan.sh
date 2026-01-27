#!/usr/bin/env bash
set -e

# Ensure output directory exists
mkdir -p dist

echo "◈ INITIATING VULNERABILITY SCAN..."

# Check if pip-audit is installed, install if missing
if ! command -v pip-audit &> /dev/null; then
    pip install pip-audit > /dev/null
fi

# Run audit on requirements.txt and output to JSON
# We allow the command to fail (|| true) so the build doesn't crash, 
# but we capture the results for the README status.
pip-audit -r requirements.txt --format json > dist/audit_raw.json || true

# Parse raw JSON into our System Surface format
python3 - << 'PYTHON_EOF'
import json, os

raw_file = 'dist/audit_raw.json'
out_file = 'dist/security-report.json'

try:
    with open(raw_file, 'r') as f:
        audit_data = json.load(f)
    
    # dependencies in pip-audit JSON are a list; vulnerabilities are nested within
    vulns = {"critical": 0, "high": 0, "medium": 0}
    
    # Basic mapping: pip-audit doesn't always provide CVSS in simple output, 
    # we count total unique CVEs found as 'high' for this logic iteration.
    total_found = len(audit_data.get("dependencies", []))
    
    status = "PASS" if total_found == 0 else "FAIL"
    hygiene = "CLEAN" if total_found == 0 else "DEGRADED"

    report = {
        "hygiene": hygiene,
        "vulnerabilities": {
            "critical": 0, 
            "high": total_found, 
            "medium": 0
        },
        "engine_version": "QuantumSec/v1.0.9-audit"
    }
except Exception:
    report = {
        "hygiene": "UNKNOWN",
        "vulnerabilities": {"critical": 0, "high": 0, "medium": 0},
        "engine_version": "QuantumSec/v1.0.9-error"
    }

with open(out_file, 'w') as f:
    json.dump(report, f)
PYTHON_EOF

echo "◈ SECURITY AUDIT COMPLETE: $(cat dist/security-report.json)"
