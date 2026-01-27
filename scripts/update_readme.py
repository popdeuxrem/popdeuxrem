#!/usr/bin/env python3
import os
import subprocess
import datetime
import json
from generate_header import generate_header as build_header
from generate_capability_matrix import generate_matrix as build_matrix
from generate_glitch_snake import generate_glitch_snake as build_glitch
from generate_visuals import generate_visuals as build_visuals
from generate_waveform import generate_waveform as build_waveform
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
        report_path = 'dist/security-report.json'
        if not os.path.exists(report_path): return "🛡️ SEC_AUDIT: PENDING"
        with open(report_path, 'r') as f:
            data = json.load(f)
            v = data['vulnerabilities']
            return f"🛡️ SEC_AUDIT: {data['hygiene']} | CRIT:{v['critical']} HIGH:{v['high']} MED:{v['medium']} | {data['engine_version']}"
    except Exception as e:
        return f"🛡️ SEC_AUDIT: ERROR_{type(e).__name__}"

def run_build():
    print("◈ INITIALIZING SYSTEM HYDRATION...")
    
    # 0. Pre-build checks & Vulnerability Scan
    if os.path.exists("scripts/vuln_scan.sh"):
        subprocess.run(["bash", "scripts/vuln_scan.sh"], check=True)
    
    # 1. Regenerate Visual Assets (v3.2 Spectre Spec)
    build_header()           # Terminal-style Header
    build_glitch()           # The Kinetic Glitch Snake
    build_matrix()           # Corrupted Capability Matrix
    build_telemetry()        # 4-Column Panel
    build_heatline()         # Activity Heatline
    build_security()         # Stamped Certificate
    build_waveform(0.8)      # Section Dividers
    
    # 2. Collect Discovery Data
    vessels = fetch_github_metrics("popdeuxrem")
    repo_url = "https://raw.githubusercontent.com/popdeuxrem/popdeuxrem/main"
    ts = int(datetime.datetime.now().timestamp())
    
    # 3. Define Hydration Data
    data = {
        "GLITCH_GLYPH": "𖢧ꛅ𖤢 ꚽꚳꛈ𖢧ꛕꛅ",
        "SKILL_MATRIX": f'<img src="{repo_url}/assets/capability-matrix.svg?v={ts}" width="800" />',
        "LAST_SYNC": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "VESSEL_MANIFEST": render_vessel_table(vessels),
        "GIT_SHA": get_git_sha(),
        "ASCII_DIVIDER": "\n```text\n[ ◈ " + ("-" * 50) + " ◈ ]\n```\n",
        "SECURITY_SUMMARY": get_security_summary(),
        "GEN_VERSION": "QuantumProfileSurface/v3.2.1",
        "SNAKE_QUOTE": f'<img src="{repo_url}/assets/glitch_snake.svg?v={ts}" width="1000" alt="Philosophy Stream" />',
        "TELEMETRY_PANEL": f'<img src="{repo_url}/assets/telemetry-panel.svg?v={ts}" width="800" alt="System Telemetry" />'
    }

    # 4. Read Template and Inject
    template_path = 'config/README.template.md'
    if not os.path.exists(template_path):
        print(f"!! CRITICAL FAILURE: {template_path} not found.")
        return

    with open(template_path, 'r') as f:
        content = f.read()

    for key, value in data.items():
        content = content.replace("{{" + key + "}}", str(value))

    # 5. Final Write
    with open('README.md', 'w') as f:
        f.write(content)
        
    print(f"◈ BUILD SUCCESSFUL | Version: {data['GEN_VERSION']} | SHA: {data['GIT_SHA']}")

if __name__ == "__main__":
    run_build()
