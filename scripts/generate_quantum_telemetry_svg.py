import os
from datetime import datetime

TELEMETRY_SVG_PATH = "assets/telemetry/quantum-telemetry.svg"

def generate_svg(metrics):
    svg = f"""
<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"400\" height=\"200\" viewBox=\"0 0 400 200\">
  <style>.header {{ font: bold 16px monospace; fill: white; }}</style>
  <rect width=\"100%\" height=\"100%\" fill=\"black\"/>
  <text class=\"header\" x=\"10\" y=\"20\">Quantum Telemetry Panel</text>
  <text class=\"header\" x=\"10\" y=\"50\">Commits: {metrics['commits']}</text>
  <text class=\"header\" x=\"10\" y=\"80\">PRs: {metrics['prs']}</text>
</svg>"""
    return svg

if __name__ == "__main__":
    metrics = {"commits": 24, "prs": 3}
    os.makedirs(os.path.dirname(TELEMETRY_SVG_PATH), exist_ok=True)
    with open(TELEMETRY_SVG_PATH, "w") as f:
        f.write(generate_svg(metrics))