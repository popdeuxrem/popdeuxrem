#!/usr/bin/env python3
import os
import requests
import json
from datetime import datetime

def fetch_github_metrics(username):
    """Fetches repository data and generates global telemetry state."""
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    
    repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=30"
    try:
        response = requests.get(repos_url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"!! DISCOVERY_ERROR: {e}")
        return []

    vessels = []
    total_issues = 0
    total_stars = 0
    
    for repo in response.json():
        if not repo['fork']:
            # Calculate freshness status
            last_update = datetime.strptime(repo['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
            days_since = (datetime.now() - last_update).days
            status = "ACTIVE" if days_since < 90 else "STABLE"
            
            vessels.append({
                "name": repo['name'],
                "desc": repo['description'] or "No description provided.",
                "description": repo['description'] or "No description provided.",
                "stars": repo['stargazers_count'],
                "stargazers_count": repo['stargazers_count'],
                "forks": repo['forks_count'],
                "forks_count": repo['forks_count'],
                "lang": repo['language'] or "Misc",
                "language": repo['language'] or "Misc",
                "url": repo['html_url'],
                "html_url": repo['html_url'],
                "status": status,
                "updated_at": repo['updated_at']
            })
            total_issues += repo.get('open_issues_count', 0)
            total_stars += repo.get('stargazers_count', 0)
            
    # Atomic write to telemetry store
    os.makedirs('dist', exist_ok=True)
    with open('dist/telemetry_data.json', 'w') as f:
        json.dump({
            "total_issues": total_issues, 
            "total_stars": total_stars,
            "repo_count": len(vessels),
            "last_audit": datetime.now().isoformat()
        }, f)
        
    return vessels

def render_vessel_table(vessels):
    """Produces GitHub-flavored markdown table for the README."""
    if not vessels:
        return "*[ ! ] No active vessels discovered in public grid.*"
    
    table = "| Vessel | Description | Stack | Metrics | Status |\n"
    table += "| :--- | :--- | :--- | :--- | :---: |\n"
    
    # Limit to top 5 for vertical economy
    for v in vessels[:5]:
        # Link to the automated vessel report created by generate_vessel_reports.py
        report_link = f"./docs/deployments/{v['name']}.md"
        table += f"| **[{v['name']}]({report_link})** | {v['desc']} | `{v['lang']}` | ⭐ {v['stars']} 🍴 {v['forks']} | `{v['status']}` |\n"
    return table

def render_skill_bars():
    """Parses skills.json into visual progress bars."""
    try:
        with open('skills.json', 'r') as f:
            skills_data = json.load(f)
        
        output = ""
        # Handle both list and category-based skills.json structures
        if isinstance(skills_data, dict):
            for category, items in skills_data.items():
                output += f"#### {category.upper()}\n"
                for s in items:
                    level = s.get('level', 8)
                    bar = "█" * level + "░" * (10 - level)
                    output += f"- {s['name']} `{bar}`\n"
                output += "\n"
        return output
    except Exception as e:
        return f"*[ ! ] Skill matrix offline: {str(e)}*"

if __name__ == "__main__":
    # Test execution
    data = fetch_github_metrics("popdeuxrem")
    print(render_vessel_table(data))
