#!/usr/bin/env python3
import os

def generate_header():
    svg_content = """<svg fill="none" viewBox="0 0 800 200" width="800" height="200" xmlns="http://www.w3.org/2000/svg">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <style>
        @keyframes scan { 0% { transform: translateY(-100%); } 100% { transform: translateY(100%); } }
        @keyframes pulse { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
        .container {
          font-family: 'Segoe UI', Ubuntu, Sans-Serif;
          background: #0d1117;
          color: #58a6ff;
          height: 198px;
          border: 1px solid #30363d;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          position: relative;
          overflow: hidden;
          border-radius: 6px;
        }
        .scanner {
          position: absolute;
          width: 100%;
          height: 2px;
          background: rgba(88, 166, 255, 0.4);
          box-shadow: 0 0 15px #58a6ff;
          animation: scan 4s linear infinite;
        }
        .title {
          font-size: 42px;
          font-weight: 800;
          letter-spacing: 12px;
          text-transform: uppercase;
          margin: 0;
          z-index: 1;
          text-shadow: 0 0 10px rgba(88, 166, 255, 0.3);
        }
        .subtitle {
          font-size: 14px;
          color: #8b949e;
          letter-spacing: 5px;
          margin-top: 10px;
          z-index: 1;
          animation: pulse 2s ease-in-out infinite;
        }
        @media (prefers-color-scheme: light) {
          .container { background: #ffffff; color: #0969da; border-color: #d0d7de; }
          .scanner { background: rgba(9, 105, 218, 0.2); box-shadow: 0 0 15px #0969da; }
          .subtitle { color: #57606a; }
        }
      </style>
      <div class="container">
        <div class="scanner"></div>
        <h1 class="title">POPDEUXREM</h1>
        <div class="subtitle">QUANTUM · PROFILE · SURFACE · V3.0</div>
      </div>
    </div>
  </foreignObject>
</svg>"""
    os.makedirs('assets', exist_ok=True)
    with open('assets/header-plate.svg', 'w') as f:
        f.write(svg_content)
    print("◈ Header evolved and regenerated.")

if __name__ == "__main__":
    generate_header()
