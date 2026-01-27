#!/usr/bin/env python3
import os

def generate_visuals():
    os.makedirs('assets', exist_ok=True)
    
    # 1. Quantum Grid Generator
    grid_svg = """<svg width="800" height="20" xmlns="http://www.w3.org/2000/svg">
  <defs><pattern id="p" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#21262D"/></pattern></defs>
  <rect width="800" height="20" fill="url(#p)"/>
  <rect y="10" width="800" height="1" fill="#30363D"/>
  <rect x="350" y="5" width="100" height="10" fill="#0D1117"/>
  <rect x="390" y="8" width="20" height="4" fill="#00FF9D" rx="2" opacity="0.6">
    <animate attributeName="opacity" values="0.2;0.8;0.2" dur="2s" repeatCount="indefinite" />
  </rect>
</svg>"""

    # 2. Animated Particle Divider Generator
    divider_svg = """<svg fill="none" viewBox="0 0 800 60" width="800" height="60" xmlns="http://www.w3.org/2000/svg">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <style>
        .divider-container { width: 800px; height: 60px; display: flex; align-items: center; justify-content: center; position: relative; background: transparent; overflow: hidden; }
        .line { width: 100%; height: 1px; background: linear-gradient(90deg, transparent, #30363d, #58a6ff, #30363d, transparent); position: relative; }
        .particle { position: absolute; width: 4px; height: 4px; background: #58a6ff; border-radius: 50%; filter: blur(1px); animation: move 3s infinite linear; }
        @keyframes move { 0% { transform: translateX(0px); opacity: 0; } 50% { opacity: 1; } 100% { transform: translateX(800px); opacity: 0; } }
        .p1 { animation-delay: 0s; top: -2px; }
        .p2 { animation-delay: 1.5s; top: -2px; }
        @media (prefers-color-scheme: light) {
          .line { background: linear-gradient(90deg, transparent, #d0d7de, #0969da, #d0d7de, transparent); }
          .particle { background: #0969da; }
        }
      </style>
      <div class="divider-container"><div class="line"><div class="particle p1"></div><div class="particle p2"></div></div></div>
    </div>
  </foreignObject>
</svg>"""

    with open('assets/bg-quantum-grid.svg', 'w') as f: f.write(grid_svg)
    with open('assets/quantum-divider.svg', 'w') as f: f.write(divider_svg)
    print("◈ Visual assets regenerated: Grid & Particle Divider.")

if __name__ == "__main__":
    generate_visuals()
