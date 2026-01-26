import os
import requests
import json
from datetime import datetime

def fetch_github_metrics(username):
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    
    repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=30"
    response = requests.get(repos_url, headers=headers)
    
    if response.status_code != 200:
        return []

    vessels = []
    total_issues = 0
    
    for repo in response.json():
        if not repo['fork']:
            vessels.append({
                "name": repo['name'],
                "desc": repo['description'] or "No description provided.",
                "stars": repo['stargazers_count'],
                "forks": repo['forks_count'],
                "lang": repo['language'] or "Misc",
                "url": repo['html_url'],
                "status": "ACTIVE" if (datetime.now() - datetime.strptime(repo['updated_at'], "%Y-%m-%dT%H:%M:%SZ")).days < 90 else "STABLE"
            })
            total_issues += repo.get('open_issues_count', 0)
            
    # Save global metrics for SVG generation
    with open('dist/telemetry_data.json', 'w') as f:
        json.dump({"total_issues": total_issues, "repo_count": len(vessels)}, f)
        
    return vessels

def render_vessel_table(vessels):
    if not vessels:
        return "*[ ! ] No active vessels discovered in public grid.*"
    table = "| Vessel | Description | Stack | Metrics | Status |\n| :--- | :--- | :--- | :--- | :---: |\n"
    for v in vessels[:5]:
        table += f"| **[{v['name']}]({v['url']})** | {v['desc']} | `{v['lang']}` | ⭐ {v['stars']} 🍴 {v['forks']} | `{v['status']}` |\n"
    return table

def render_skill_bars():
    try:
        with open('skills.json', 'r') as f:
            skills = json.load(f)
        output = ""
        for area, items in skills.items():
            output += f"### {area}\n"
            for s in items:
                level = s.get('level', 8)
                bar = "█" * level + "░" * (10 - level)
                output += f"- {s['name']} `{bar}`\n"
        return output
    except:
        return ""
