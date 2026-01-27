#!/usr/bin/env python3
import os

def generate_glitch_header():
    # Glyph: 𖢧ꛅ𖤢 ꚽꚳꛈ𖢧ꛕꛅ (THE GLITCH)
    svg = """<svg width="800" height="150" viewBox="0 0 800 150" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glitch">
      <feFlood flood-color="#00f3ff" result="flood1" />
      <feFlood flood-color="#9d00ff" result="flood2" />
      <feOffset in="SourceGraphic" dx="2" result="off1" />
      <feOffset in="SourceGraphic" dx="-2" result="off2" />
      <feComposite in="flood1" in2="off1" operator="in" result="comp1" />
      <feComposite in="flood2" in2="off2" operator="in" result="comp2" />
      <feMerge>
        <feMergeNode in="comp1" />
        <feMergeNode in="comp2" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
      <animate attributeName="dx" values="0;2;0;-2;0" dur="0.2s" repeatCount="indefinite" />
    </filter>
  </defs>
  
  <rect width="800" height="150" rx="12" fill="#0a0a0f" stroke="#30363d"/>
  <text x="30" y="70" font-family="monospace" font-size="38" font-weight="bold" fill="#ffffff" filter="url(#glitch)">
    𖢧ꛅ𖤢 ꚽꚳꛈ𖢧ꛕꛅ <tspan fill="#9d00ff">· V3.1</tspan>
  </text>
  <text x="35" y="110" font-family="monospace" font-size="14" fill="#00f3ff" opacity="0.6" letter-spacing="4">
    SYSTEM_REGENERATED // ARCHITECT_OVERRIDE
  </text>
  
  <rect x="620" y="30" width="150" height="30" rx="4" fill="#161b22" stroke="#4ade80" stroke-opacity="0.5"/>
  <text x="635" y="50" font-family="monospace" font-size="11" fill="#4ade80">● SIGNAL_STABLE</text>
</svg>"""
    os.makedirs('assets', exist_ok=True)
    with open('assets/header-plate.svg', 'w') as f:
        f.write(svg)

if __name__ == "__main__":
    generate_glitch_header()
