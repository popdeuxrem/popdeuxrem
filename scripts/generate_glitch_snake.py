#!/usr/bin/env python3
import os
import json

def generate_glitch_snake():
    # Detect System State
    is_alert = False
    try:
        with open('dist/security-report.json', 'r') as f:
            sec_data = json.load(f)
            v = sec_data.get('vulnerabilities', {})
            is_alert = v.get('critical', 0) > 0 or v.get('high', 0) > 0
    except:
        pass

    # Dynamic Parameters
    glyph = "𖢧ꛅ𖤢 ꚽꚳꛈ𖢧ꛕꛅ"
    primary_color = "#ff0000" if is_alert else "#ffffff"
    accent_color = "#8b0000" if is_alert else "#00f3ff"
    speed = "0.05s" if is_alert else "0.15s"
    scale = "60" if is_alert else "30"

    svg = f"""<svg width="1000" height="200" viewBox="0 0 1000 200" xmlns="http://www.w3.org/2000/svg">
  <rect width="1000" height="200" fill="#0d1117"/>
  <defs>
    <filter id="f1">
      <feTurbulence type="fractalNoise" baseFrequency="0.01 0.4" numOctaves="2" result="warp">
        <animate attributeName="baseFrequency" values="0.01 0.4;0.1 0.3;0.01 0.4" dur="{speed}" repeatCount="indefinite" />
      </feTurbulence>
      <feDisplacementMap xChannelSelector="R" yChannelSelector="G" scale="{scale}" in="SourceGraphic" in2="warp" />
    </filter>
  </defs>

  <g opacity="0.4">
    <text x="0" y="180" font-family="monospace" font-size="14" fill="{accent_color}">
      <tspan>🜂 ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─ ─ ◈ ─</tspan>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-200 0" dur="2s" repeatCount="indefinite" />
    </text>
  </g>

  <g font-family="monospace" font-size="64" font-weight="bold" text-anchor="middle" dominant-baseline="middle">
    <text x="502" y="100" fill="#ff0000" opacity="0.8" filter="url(#f1)">{glyph}</text>
    <text x="498" y="100" fill="{accent_color}" opacity="0.8" filter="url(#f1)">{glyph}</text>
    <text x="500" y="100" fill="{primary_color}">{glyph}</text>
  </g>
  
  {"<rect width='1000' height='200' fill='red' opacity='0.05' filter='url(#f1)'/>" if is_alert else ""}
</svg>"""

    os.makedirs('assets', exist_ok=True)
    with open('assets/glitch_snake.svg', 'w') as f:
        f.write(svg)
    print(f"◈ Glitch Snake generated. Mode: {'ALERT' if is_alert else 'NOMINAL'}")

if __name__ == "__main__":
    generate_glitch_snake()
