import json
import os
from datetime import datetime

def generate_security_svg():
    report_path = 'dist/security-report.json'
    
    # Default state if report is missing
    data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "vulnerabilities": {"critical": 0, "high": 0, "medium": 0},
        "hygiene": "UNKNOWN",
        "engine_version": "QuantumSec/v1.0.0"
    }

    if os.path.exists(report_path):
        with open(report_path, 'r') as f:
            data = json.load(f)

    # Color Logic
    v_total = sum(data['vulnerabilities'].values())
    status_color = "#238636" # Green
    if v_total > 0 or data['hygiene'] == "WARN":
        status_color = "#d29922" # Yellow
    if data['vulnerabilities']['critical'] > 0:
        status_color = "#f85149" # Red

    svg = f"""<svg width="800" height="150" viewBox="0 0 800 150" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .base {{ font-family: 'JetBrains Mono', monospace; font-size: 13px; fill: #8b949e; }}
    .header {{ font-family: 'JetBrains Mono', monospace; font-size: 14px; fill: #f85149; font-weight: bold; }}
    .value {{ fill: #c9d1d9; }}
    .border {{ stroke: #30363d; }}
    @media (prefers-color-scheme: light) {{
      .value {{ fill: #24292f; }}
      .border {{ stroke: #d0d7de; }}
    }}
  </style>
  <rect x="0.5" y="0.5" width="799" height="149" rx="5" class="border" fill="transparent"/>
  
  <text x="20" y="35" class="header">SECURITY TELEMETRY :: AUDIT_REPORT</text>
  <path d="M20 50H780" stroke="#30363d" />

  <text x="20" y="80" class="base">VULNERABILITIES:</text>
  <text x="160" y="80" class="value">CRIT:{data['vulnerabilities']['critical']} | HIGH:{data['vulnerabilities']['high']} | MED:{data['vulnerabilities']['medium']}</text>
  
  <text x="400" y="80" class="base">REPO_HYGIENE:</text>
  <text x="540" y="80" class="value">{data['hygiene']}</text>

  <text x="20" y="115" class="base">SCAN_TIMESTAMP:</text>
  <text x="160" y="115" class="value">{data['timestamp']}</text>
  
  <rect x="540" y="102" width="120" height="18" rx="3" fill="{status_color}"/>
  <text x="548" y="115" style="fill:white; font-size:11px; font-weight:bold;">SEC_STATUS: {data['hygiene']}</text>
  
  <text x="680" y="135" style="fill:#484f58; font-size:10px;">{data['engine_version']}</text>
</svg>"""

    with open('assets/security-status.svg', 'w') as f:
        f.write(svg)

if __name__ == "__main__":
    generate_security_svg()
