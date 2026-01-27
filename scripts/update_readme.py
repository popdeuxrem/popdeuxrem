#!/usr/bin/env python3
import os
import subprocess
import datetime
import json

# Component Generators
from generate_header import generate_header as build_header
from generate_glitch_snake import generate_glitch_snake as build_glitch
from generate_capability_matrix import generate_matrix as build_matrix
from generate_telemetry_panel import generate_panel_svg as build_telemetry
from generate_heatline import generate_heatline_svg as build_heatline
from generate_security_svg import generate_security_svg as build_security
from generate_waveform import generate_waveform as build_waveform
from generate_visuals import generate_visuals as build_visuals
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
    print("◈ INITIALIZING SPECTRE HYDRATION...")
    
    # 0. Pre-build logic
    subprocess.run(["bash", "scripts/vuln_scan.sh"], check=False)
    subprocess.run(["bash", "scripts/terminal_shot.sh"], check=False)
    
    # 1. Regenerate Visual Assets
    build_header()
    build_glitch()
    build_matrix()
    build_telemetry()
    build_heatline()
    build_security()
    build_waveform(0.8)
    build_visuals()
    
    # 2. Setup Context
    vessels = fetch_github_metrics("popdeuxrem")
    repo_url = "https://raw.githubusercontent.com/popdeuxrem/popdeuxrem/main"
    ts = int(datetime.datetime.now().timestamp())
    
    # 3. Payload mapping
    data = {
        "GLITCH_GLYPH": "𖢧ꛅ𖤢 ꚽꚳꛈ𖢧ꛕꛅ",
        "SKILL_MATRIX": f'<img src="{repo_url}/assets/capability-matrix.svg?v={ts}" width="800" alt="Skill Matrix" />',
        "LAST_SYNC": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "VESSEL_MANIFEST": render_vessel_table(vessels),
        "GIT_SHA": get_git_sha(),
        "SECURITY_SUMMARY": get_security_summary(),
        "GEN_VERSION": "QuantumProfileSurface/v3.2.1",
        "GLITCH_SNAKE": f'<img src="{repo_url}/assets/glitch_snake.svg?v={ts}" width="1000" alt="THE GLITCH" />',
        "TELEMETRY_PANEL": f'<img src="{repo_url}/assets/telemetry-panel.svg?v={ts}" width="800" alt="Telemetry" />',
        "ASCII_DIVIDER": "\n```text\n[ ◈ " + ("-" * 50) + " ◈ ]\n```\n"
    }

    # 4. Inject into Template
    with open('config/README.template.md', 'r') as f:
        content = f.read()
    for key, value in data.items():
        content = content.replace("{{" + key + "}}", str(value))
    
    with open('README.md', 'w') as f:
        f.write(content)
    print(f"◈ DEPLOYED v3.2.1 | SHA: {data['GIT_SHA']}")

if __name__ == "__main__":
    run_build()
