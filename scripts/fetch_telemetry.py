import os
import requests
from datetime import datetime, timedelta

def get_architect_metrics(username="popdeuxrem"):
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    
    # 1. Repo Velocity (30-day commit count)
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
    events_url = f"https://api.github.com/users/{username}/events"
    
    commits_30d = 0
    try:
        events = requests.get(events_url, headers=headers).json()
        for event in events:
            if event['type'] == 'PushEvent':
                created_at = event['created_at']
                if created_at > thirty_days_ago:
                    commits_30d += len(event['payload'].get('commits', []))
    except:
        commits_30d = "ERR"

    # 2. Signal Ratio (Issues Closed vs Total)
    search_url = f"https://api.github.com/search/issues?q=user:{username}+is:issue"
    try:
        total_issues = requests.get(search_url, headers=headers).json().get('total_count', 0)
        closed_issues = requests.get(search_url + "+is:closed", headers=headers).json().get('total_count', 0)
        signal_ratio = f"{(closed_issues/total_issues)*100:.1f}%" if total_issues > 0 else "100%"
    except:
        signal_ratio = "100%"

    return {
        "velocity": f"{commits_30d} commits/mo",
        "signal": signal_ratio,
        "cadence": datetime.now().strftime("%H:%M UTC")
    }

if __name__ == "__main__":
    print(get_architect_metrics())
