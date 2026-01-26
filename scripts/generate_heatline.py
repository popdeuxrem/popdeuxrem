import os
import requests
from datetime import datetime, timedelta

def generate_heatline_svg(username="popdeuxrem"):
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    
    # Fetch last 100 events to approximate daily activity
    url = f"https://api.github.com/users/{username}/events"
    data = [0] * 14  # 14-day window
    today = datetime.now().date()

    try:
        events = requests.get(url, headers=headers).json()
        for event in events:
            created_at = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ").date()
            delta = (today - created_at).days
            if 0 <= delta < 14:
                data[13 - delta] += 1
    except:
        pass

    # SVG Construction
    width = 800
    height = 40
    step = width / 14
    max_val = max(data) if max(data) > 0 else 1
    
    svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    svg += '<style>.bar { fill: #238636; opacity: 0.6; } .label { font-family: monospace; font-size: 10px; fill: #8b949e; }</style>'
    
    for i, val in enumerate(data):
        h = (val / max_val) * (height - 15)
        x = i * step
        opacity = 0.2 + (val / max_val) * 0.8
        svg += f'<rect x="{x}" y="{height - h - 10}" width="{step - 4}" height="{h}" rx="2" class="bar" style="opacity: {opacity}" />'
    
    svg += f'<text x="0" y="{height}" class="label">14D_ACTIVITY_TRANSIT</text>'
    svg += f'<text x="{width-60}" y="{height}" class="label">LIVE_SIGNAL</text>'
    svg += '</svg>'

    with open('assets/activity-heatline.svg', 'w') as f:
        f.write(svg)

if __name__ == "__main__":
    generate_heatline_svg()
