import requests
import os

def fetch_quantum_vessels(username="popdeuxrem"):
    """
    Query GitHub API for repositories tagged with 'quantum-vessel'.
    Returns a list of dictionaries for README injection.
    """
    # Use GITHUB_TOKEN if available in Actions, otherwise anonymous
    headers = {}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=100"
    vessels = []
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos = response.json()
            for repo in repos:
                # Filter by topic: quantum-vessel
                if "quantum-vessel" in repo.get("topics", []):
                    vessels.append({
                        "name": repo["name"],
                        "url": repo["html_url"],
                        "desc": repo["description"] or "No description provided.",
                        "stars": repo["stargazers_count"],
                        "lang": repo["language"] or "Misc"
                    })
    except Exception as e:
        print(f"◈ DISCOVERY ERROR: {e}")
        
    return vessels

def format_vessel_table(vessels):
    if not vessels:
        return "*No active vessels discovered in public grid.*"
    
    table = "| Vessel ID | Classification | Intelligence | Status |\n"
    table += "| :--- | :--- | :--- | :---: |\n"
    for v in vessels:
        table += f"| **[{v['name']}]({v['url']})** | {v['lang']} | {v['desc']} | `⭐ {v['stars']}` |\n"
    return table
