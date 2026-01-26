import os
import subprocess
import datetime
import json
from generate_snake_quote import generate_svg as build_snake_quote
from generate_telemetry_panel import generate_panel_svg as build_telemetry
from generate_heatline import generate_heatline_svg as build_heatline
from generate_security_svg import generate_security_svg as build_security
from discovery import fetch_github_metrics, render_vessel_table, render_skill_bars

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
        return "🛡️ SEC_AUDIT: PENDING"

def run_build():
    print("◈ INITIALIZING SYSTEM HYDRATION...")
    subprocess.run(["bash", "scripts/vuln_scan.sh"], check=True)
    
    build_snake_quote()
    build_telemetry()
    build_heatline()
    build_security()
    
    vessels = fetch_github_metrics("popdeuxrem")
    
    data = {
        "SKILL_MATRIX": render_skill_bars(),
        "LAST_SYNC": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "VESSEL_MANIFEST": render_vessel_table(vessels),
        "GIT_SHA": get_git_sha(),
        "ASCII_DIVIDER": "\n```text\n[ ◈ " + ("-" * 50) + " ◈ ]\n```\n",
        "SECURITY_SUMMARY": get_security_summary()
    }

    with open('config/README.template.md', 'r') as f:
        content = f.read()

    for key, value in data.items():
        content = content.replace("{{" + key + "}}", str(value))

    with open('README.md', 'w') as f:
        f.write(content)
    print(f"◈ BUILD SUCCESSFUL | SHA: {data['GIT_SHA']}")

if __name__ == "__main__":
    run_build()
