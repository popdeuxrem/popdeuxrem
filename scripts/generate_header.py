#!/usr/bin/env python3
import os

def generate_header():
    svg_content = """<svg width="800" height="150" viewBox="0 0 800 150" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="150" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="2"/>
  <path d="M0 12C0 5.37258 5.37258 0 12 0H788C794.627 0 800 5.37258 800 12V40H0V12Z" fill="#161b22"/>
  <circle cx="20" cy="20" r="5" fill="#ff5f56"/><circle cx="40" cy="20" r="5" fill="#ffbd2e"/><circle cx="60" cy="20" r="5" fill="#27c93f"/>
  <text x="400" y="25" text-anchor="middle" font-family="monospace" font-size="12" fill="#8b949e">popdeuxrem@system:~/surface</text>
  
  <text x="30" y="85" font-family="sans-serif" font-size="32" font-weight="bold" fill="#ffffff">
    <tspan fill="#00f3ff">#</tspan> QUANTUM SURFACE <tspan fill="#9d00ff">· V3.0</tspan>
  </text>
  <text x="35" y="115" font-family="monospace" font-size="14" fill="#00f3ff" opacity="0.8">Principal Engineer &amp; Product Architect</text>
  
  <rect x="620" y="70" width="150" height="35" rx="6" fill="#000000"/>
  <text x="635" y="92" font-family="monospace" font-size="12" fill="#4ade80">$ status --online</text>
  <circle cx="755" cy="87" r="4" fill="#4ade80">
    <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite" />
  </circle>
</svg>"""
    os.makedirs('assets', exist_ok=True)
    with open('assets/header-plate.svg', 'w') as f:
        f.write(svg_content)
    print("◈ Header refactored to Tailwind spec.")

if __name__ == "__main__":
    generate_header()
