#!/usr/bin/env python3
import os
import random

def generate_waveform(activity_level=1):
    # Map activity_level (0.0 to 1.0) to animation duration (3s to 0.5s)
    duration = max(0.5, 3.0 - (activity_level * 2.5))
    color = "#58a6ff" if activity_level < 0.7 else "#00FF9D" # Shift to Green on high activity
    
    svg_content = f"""<svg width="800" height="60" viewBox="0 0 800 60" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M0 30H300L310 10L325 50L340 30H360L370 20L385 40L400 30H800" stroke="{color}" stroke-width="2" stroke-opacity="0.3" />
  <path d="M0 30H300L310 10L325 50L340 30H360L370 20L385 40L400 30H800" stroke="{color}" stroke-width="2">
    <animate attributeName="stroke-dasharray" from="0,1000" to="1000,0" dur="{duration}s" repeatCount="indefinite" />
  </path>
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
</svg>"""

    os.makedirs('assets', exist_ok=True)
    with open('assets/divider-waveform.svg', 'w') as f:
        f.write(svg_content)
    print(f"◈ Waveform generated: Pulse Speed {duration}s | Color {color}")

if __name__ == "__main__":
    generate_waveform(0.5) # Default mid-tempo
