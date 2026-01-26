import os
import requests
import json
from datetime import datetime

def fetch_github_metrics(username):
    """Fetches real-time repo data and PR/Issue counts."""
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    
    # Fetch Repositories
    repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
    response = requests.get(repos_url, headers=headers)
    
    if response.status_code != 200:
        return []

    vessels = []
    for repo in response.json():
        if not repo['fork']:  # Focus on original works
            vessels.append({
                "name": repo['name'],
                "desc": repo['description'] or "No description provided.",
                "stars": repo['stargazers_count'],
                "forks": repo['forks_count'],
                "lang": repo['language'] or "Misc",
                "url": repo['html_url'],
                "status": "ACTIVE" if (datetime.now() - datetime.strptime(repo['updated_at'], "%Y-%m-%dT%H:%M:%SZ")).days < 90 else "STABLE"
            })
    return vessels

def render_vessel_table(vessels):
    if not vessels:
        return "*[ ! ] No active vessels discovered in public grid.*"
    
    table = "| Vessel | Description | Stack | Metrics | Status |\n"
    table += "| :--- | :--- | :--- | :--- | :---: |\n"
    for v in vessels[:5]: # Top 5
        metrics = f"⭐ {v['stars']} 🍴 {v['forks']}"
        table += f"| **[{v['name']}]({v['url']})** | {v['desc']} | `{v['lang']}` | {metrics} | `{v['status']}` |\n"
    return table

def render_skill_bars():
    """Parses skills.json into visual progress bars."""
    try:
        with open('skills.json', 'r') as f:
            skills = json.load(f)
        
        output = "\n"
        for area, items in skills.items():
            output += f"**{area}**\n"
            for s in items:
                # Simple ASCII bar based on a 'level' key if it exists, else 80%
                level = s.get('level', 8) 
                bar = "█" * level + "░" * (10 - level)
                output += f"- {s['name']} `{bar}`\n"
            output += "\n"
        return output
    except Exception as e:
        return f""

if __name__ == "__main__":
    # Test execution
    data = fetch_github_metrics("popdeuxrem")
    print(render_vessel_table(data))
