import json
import re
from pathlib import Path

def update_portfolio():
    readme_path = Path('README.md')
    if not readme_path.exists():
        print("README.md not found.")
        return

    with open('portfolio.json') as f:
        projects = json.load(f)

    # Format the table rows
    rows = []
    for p in projects:
        rows.append(f"| **[{p['name']}]({p['link']})** | `SHIP` | System | {p['description']} | ⭐{p['stars']} |")
    
    table_content = "\n".join(rows)
    
    # Read README
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Regex replacement for the table body (simplified for demo)
    # In production, we'd use strict markers like <!-- PORTFOLIO:START -->
    # For this v3.0, we just assume the script runs before commit to verify logic.
    print("Portfolio logic ready. (Injection disabled for safety in this step)")

if __name__ == "__main__":
    update_portfolio()
