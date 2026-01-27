#!/usr/bin/env python3
import os

def write_svg(name, content):
    os.makedirs('assets', exist_ok=True)
    with open(f'assets/{name}.svg', 'w') as f:
        f.write(content)

# 1. HERO (Identity) - Horizontal motion only
write_svg('snake-quote', f'''<svg width="1000" height="120" viewBox="0 0 1000 120" xmlns="http://www.w3.org/2000/svg">
<rect width="1000" height="120" fill="#0d1117"/>
<text x="0" y="75" font-family="sans-serif" font-size="42" fill="#58a6ff" font-weight="900" style="letter-spacing:2px">
  𖢧ꛅ𖤢 ꚽꚳꛈ𖢧ꛕꛅ ◈ SYSTEMS DESIGNER ◈ PRODUCT ARCHITECT ◈ AUTOMATION ENGINEER
  <animate attributeName="x" from="1000" to="-2200" dur="18s" repeatCount="indefinite" />
</text>
</svg>''')

# 2. THESIS (Terminal) - Static CLI
write_svg('thesis-terminal', f'''<svg width="800" height="300" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
<rect width="800" height="300" rx="8" fill="#161b22" stroke="#30363d"/>
<circle cx="20" cy="20" r="5" fill="#ff5f56"/><circle cx="40" cy="20" r="5" fill="#ffbd2e"/><circle cx="60" cy="20" r="5" fill="#27c93f"/>
<text x="25" y="65" font-family="monospace" font-size="15" fill="#39d353">
  <tspan x="25" dy="1.2em">root@quantum:~# cat philosophy.core</tspan>
  <tspan x="25" dy="2.0em" fill="#8b949e">01. Eliminate unnecessary abstractions.</tspan>
  <tspan x="25" dy="1.4em" fill="#8b949e">02. Observability is the prerequisite for control.</tspan>
  <tspan x="25" dy="1.4em" fill="#8b949e">03. Code is a liability; systems are the asset.</tspan>
  <tspan x="25" dy="2.0em" fill="#ffffff">INTENT: HIGH_AVAILABILITY_SURFACE</tspan>
  <tspan x="25" dy="1.4em" fill="#58a6ff">█</tspan>
</text>
</svg>''')

# 3. STACK (Grid) - Pure geometry
write_svg('stack-grid', f'''<svg width="800" height="400" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<rect width="800" height="400" fill="#0d1117"/>
<g stroke="#30363d" stroke-width="0.5">
  <path d="M0 100h800M0 200h800M0 300h800M200 0v400M400 0v400M600 0v400"/>
</g>
<g font-family="monospace" font-size="13" fill="#ffffff" text-anchor="middle" font-weight="bold">
  <text x="100" y="60">RUST</text><text x="300" y="60">GOLANG</text><text x="500" y="60">PYTHON</text><text x="700" y="60">TS/JS</text>
  <text x="100" y="160">DOCKER</text><text x="300" y="160">K8S</text><text x="500" y="160">TERRAFORM</text><text x="700" y="160">AWS/GCP</text>
  <text x="100" y="260">POSTGRES</text><text x="300" y="260">REDIS</text><text x="500" y="260">KAFKA</text><text x="700" y="260">GRPC</text>
  <text x="100" y="360">CI/CD</text><text x="300" y="360">EBPF</text><text x="500" y="360">OPENTELEMETRY</text><text x="700" y="360">SOLIDITY</text>
</g>
</svg>''')

# 4. WORK (Timeline) - Vertical flow
write_svg('work-timeline', f'''<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
<rect width="600" height="600" fill="#0d1117"/>
<path d="M120 50v500" stroke="#30363d" stroke-dasharray="4 4"/>
<circle cx="120" cy="100" r="6" fill="#f0883e"/>
<text x="145" y="105" font-family="sans-serif" fill="#ffffff" font-size="20" font-weight="bold">SPECTRE SURFACE v4.1</text>
<text x="145" y="130" font-family="sans-serif" fill="#8b949e" font-size="14">Core Infrastructure Engine</text>
<circle cx="120" cy="280" r="6" fill="#f0883e"/>
<text x="145" y="285" font-family="sans-serif" fill="#ffffff" font-size="20" font-weight="bold">STEALTH PROXY SYSTEM</text>
<text x="145" y="310" font-family="sans-serif" fill="#8b949e" font-size="14">Network Obfuscation Layer</text>
<circle cx="120" cy="460" r="6" fill="#f0883e"/>
<text x="145" y="465" font-family="sans-serif" fill="#ffffff" font-size="20" font-weight="bold">PHOTEXT PLATFORM</text>
<text x="145" y="490" font-family="sans-serif" fill="#8b949e" font-size="14">Digital Content API</text>
</svg>''')

# 5. TELEMETRY (Dashboard) - Multi-panel pulse
write_svg('telemetry-dashboard', f'''<svg width="900" height="450" viewBox="0 0 900 450" xmlns="http://www.w3.org/2000/svg">
<rect width="900" height="450" rx="4" fill="#161b22"/>
<g stroke="#30363d" fill="#0d1117">
  <rect x="20" y="20" width="280" height="410"/>
  <rect x="320" y="20" width="560" height="195"/>
  <rect x="320" y="235" width="560" height="195"/>
</g>
<circle cx="160" cy="225" r="40" fill="none" stroke="#1f6feb" stroke-width="2">
  <animate attributeName="r" values="40;45;40" dur="2s" repeatCount="indefinite" />
  <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite" />
</circle>
<text x="340" y="55" font-family="monospace" fill="#58a6ff" font-size="14">SYSTEM_LOAD: NOMINAL</text>
<path d="M340 150 l20-30 20 40 20-60 20 20 20-10" fill="none" stroke="#238636" stroke-width="2"/>
</svg>''')

# 6. SECURITY (Status) - LCD Strip
write_svg('security-status', f'''<svg width="1000" height="50" viewBox="0 0 1000 50" xmlns="http://www.w3.org/2000/svg">
<rect width="1000" height="50" fill="#0d1117" stroke="#238636" stroke-width="2"/>
<text x="25" y="32" font-family="monospace" font-size="18" fill="#238636" font-weight="bold">
  [ PASS ] SECURITY_AUDIT_V4 // VULNERABILITIES: 0 // INTEGRITY: 100% // SIGNATURE: VERIFIED
</text>
</svg>''')
