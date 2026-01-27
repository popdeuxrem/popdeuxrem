#!/usr/bin/env python3
import json, random, os

def generate_axiom():
    quotes_path = 'data/quotes.json'
    quote = random.choice(json.load(open(quotes_path))) if os.path.exists(quotes_path) else "SYSTEM_NOMINAL"
    
    svg_content = f"""<svg width="800" height="60" viewBox="0 0 800 60" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .axiom {{ font-family: 'Courier New', monospace; font-size: 14px; fill: #e0e0e0; text-transform: uppercase; letter-spacing: 3px; }}
    .glow {{ filter: drop-shadow(0 0 5px rgba(0, 243, 255, 0.5)); }}
  </style>
  <rect x="100" y="10" width="600" height="40" rx="20" fill="#0d1117" stroke="#9d00ff" stroke-opacity="0.3"/>
  <text x="400" y="35" text-anchor="middle" class="axiom glow">
    <tspan fill="#00f3ff">≫</tspan> {quote} <tspan fill="#00f3ff">≪</tspan>
  </text>
</svg>"""
    with open('assets/random-axiom.svg', 'w') as f: f.write(svg_content)
    print("◈ Axiom visual updated.")

if __name__ == "__main__":
    generate_axiom()
