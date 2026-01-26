import os
import subprocess
import datetime
import random
import json

# Import sub-generators
from generate_snake_quote import generate_svg as build_snake_quote
from generate_telemetry_panel import generate_panel_svg as build_telemetry
from generate_heatline import generate_heatline_svg as build_heatline
from generate_security_svg import generate_security_svg as build_security
from generate_metrics import generate_skill_matrix, get_system_uptime
from discovery import fetch_quantum_vessels, format_vessel_table

def get_git_sha():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    except:
        return "DEV-UNCOMMITTED"

def get_security_summary():
    try:
        with open('dist/security-report.json', 'r') as f:
            data = json.load(f)
            v = data['vulnerabilities']
            return f"🛡️ SEC_AUDIT: {data['hygiene']} | CRIT:{v['critical']} HIGH:{v['high']} MED:{v['medium']} | {data['engine_version']}"
    except:
        return "🛡️ SEC_AUDIT: PENDING_INITIAL_SCAN"

def run_build():
    print("◈ INITIALIZING SYSTEM HYDRATION...")
    
    # 1. Run Security Scan (Bash)
    subprocess.run(["bash", "scripts/vuln_scan.sh"], check=True)
    
    # 2. Generate Sub-Assets
    build_snake_quote()
    build_telemetry()
    build_heatline()
    build_security()
    
    # 3. Collect Dynamic Data
    vessels = discovery.fetch_github_metrics("popdeuxrem")
    
    # 4. Prepare Metadata
    now = datetime.datetime.now(datetime.timezone.utc)
    data = {
        "SKILL_MATRIX": generate_skill_matrix(),
        "UPTIME": get_system_uptime(),
        "LAST_SYNC": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "STATUS": "NOMINAL",
        "VESSEL_MANIFEST": discovery.render_vessel_table(vessels),
        "GIT_SHA": get_git_sha(),
        "ASCII_DIVIDER": "\n```text\n[ ◈ " + ("-" * 50) + " ◈ ]\n```\n",
        "GEN_VERSION": "QuantumProfileSurface/v3.0",
        "SECURITY_SUMMARY": get_security_summary()
    }

    # 5. Assemble README from Template
    with open('config/README.template.md', 'r') as f:
        content = f.read()

    for key, value in data.items():
        content = content.replace("{{" + key + "}}", str(value))

    with open('README.md', 'w') as f:
        f.write(content)

    print(f"◈ BUILD COMPLETE | SHA: {data['GIT_SHA']} | {data['LAST_SYNC']}")

if __name__ == "__main__":
    run_build()
