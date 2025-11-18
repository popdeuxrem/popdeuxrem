import requests
import os

LABS_MARKER = "<!-- zone:labs-ops-kits:start -->\n"

def fetch_top_repos():
    token = os.getenv("GITHUB_TOKEN")
    url = "https://api.github.com/users/popdeuxrem/repos"
    headers = {"Authorization": f"Bearer {token}"}
    repos = requests.get(url, headers=headers).json()
    return sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:3]

def format_repos(repos):
    return "\n".join([f"- [{repo['name']}]({repo['html_url']}) — {repo['description']}" for repo in repos]) + "\n"

if __name__ == "__main__":
    top_repos = fetch_top_repos()
    formatted_repos = format_repos(top_repos)
    with open("README.md", "r") as f:
        readme = f.read()
    labs_section = LABS_MARKER + formatted_repos
    updated_readme = readme.replace(LABS_MARKER, labs_section)
    with open("README.md", "w") as f:
        f.write(updated_readme)