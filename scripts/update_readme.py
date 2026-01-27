#!/usr/bin/env python3
import os
import subprocess
import datetime
import json
import time

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

def get_security_data():
    try:
        with open('dist/security-report.json', 'r') as f:
            return json.load(f)
    except:
        return {"hygiene": "UNKNOWN", "vulnerabilities": {"critical": 0, "high": 0}}

def run_build():
    print("◈ INITIALIZING SPECTRE v4.1 HYDRATION [ALERT_AWARE]...")
    
    # 0. Execute Scan
    subprocess.run(["bash", "scripts/vuln_scan.sh"], check=False)
    sec_data = get_security_data()
    v = sec_data['vulnerabilities']
    
    # 1. Determine System State (Alert Logic)
    # If CRIT > 0 or HIGH > 0, system enters ALERT status
    is_alert = v['critical'] > 0 or v['high'] > 0
    glyph_color = "#ff0000" if is_alert else "#00f3ff"
    status_label = "BREACH_RISK" if is_alert else "NOMINAL"
    
    # 2. Regenerate Visual Assets
    build_header()
    build_glitch() # We can pass glyph_color here if script is updated to accept it
    build_matrix()
    build_telemetry()
    build_heatline()
    build_security()
    build_waveform(0.8)
    build_visuals()
    
    # 3. Context & Payload Mapping
    vessels = fetch_github_metrics("popdeuxrem")
    repo_url = "https://raw.githubusercontent.com/popdeuxrem/popdeuxrem/main"
    ts = int(time.time())
    
    sec_summary = f"🛡️ SEC_AUDIT: {sec_data['hygiene']} | CRIT:{v['critical']} HIGH:{v['high']} | STATUS: {status_label}"

    data = {
        "GLITCH_GLYPH": f'<span style="color:{glyph_color}">𖢧ꛅ𖤢 ꚽꚳꛈ𖢧ꛕꛅ</span>',
        "GLITCH_SNAKE": f'<img src="{repo_url}/assets/glitch_snake.svg?v={ts}" width="1000" alt="THE GLITCH" />',
        "TELEMETRY_PANEL": f'<img src="{repo_url}/assets/telemetry-panel.svg?v={ts}" width="800" alt="Telemetry" />',
        "SKILL_MATRIX": f'<img src="{repo_url}/assets/capability-matrix.svg?v={ts}" width="800" />',
        "VESSEL_MANIFEST": render_vessel_table(vessels),
        "SECURITY_SUMMARY": sec_summary,
        "GIT_SHA": get_git_sha(),
        "LAST_SYNC": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "GEN_VERSION": "QuantumProfileSurface/v4.1-AlertAware"
    }

    # 4. Hydration
    with open('config/README.template.md', 'r') as f:
        content = f.read()

    for key, value in data.items():
        content = content.replace("{{" + key + "}}", str(value))

    with open('README.md', 'w') as f:
        f.write(content)
        
    print(f"◈ DEPLOYMENT SUCCESSFUL | STATE: {status_label} | SHA: {data['GIT_SHA']}")

if __name__ == "__main__":
    run_build()
