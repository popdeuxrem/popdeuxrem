import json
import datetime
import os

def generate_svg():
    # 1. Load Quotes
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(base_path, 'data/quotes.json'), 'r') as f:
        quotes = json.load(f)

    # 2. Deterministic Daily Selection
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    quote_data = quotes[day_of_year % len(quotes)]
    full_text = f"▸ “{quote_data['text']}” — {quote_data['author']}"
    
    # 3. Text Metrics (Approximation for monospace)
    char_width = 12 # 20px font monospace approx width
    text_width = len(full_text) * char_width
    end_x = -(text_width + 200)

    # 4. Construct SVG
    svg_template = f"""<svg fill="none" viewBox="0 0 1200 80" width="1200" height="80" xmlns="http://www.w3.org/2000/svg">
  <title>Rotating system philosophy quote</title>
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500&amp;display=swap');
      
      .quote-container {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 500;
        letter-spacing: 0.04em;
      }}

      @keyframes snake-scroll {{
        from {{ transform: translateX(1200px); }}
        to {{ transform: translateX({end_x}px); }}
      }}

      #snake-quote {{
        animation: snake-scroll 40s linear infinite;
        will-change: transform;
      }}

      .accent {{ fill: #58A6FF; }}
      .quote {{ fill: #E6EDF3; }}

      @media (prefers-color-scheme: light) {{
        .accent {{ fill: #0969DA; }}
        .quote {{ fill: #24292F; }}
      }}
    </style>
  </defs>

  <g id="snake-quote" class="quote-container">
    <text y="40" dominant-baseline="middle">
      <tspan class="accent">▸ </tspan>
      <tspan class="quote">{quote_data['text']} — {quote_data['author']}</tspan>
    </text>
  </g>
</svg>"""

    output_path = os.path.join(base_path, 'assets/snake-quote.svg')
    with open(output_path, 'w') as f:
        f.write(svg_template)
    print(f"◈ Snake-Quote Generated: {output_path}")

if __name__ == "__main__":
    generate_svg()
