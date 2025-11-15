#!/usr/bin/env python3
"""Update README with recent GitHub public activity."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from typing import List, Set, Tuple
from urllib import error, request

USER = os.getenv("RECENT_ACTIVITY_USER", "thugger069")
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(REPO_ROOT, "README.md")
FALLBACK_PATH = os.path.join(REPO_ROOT, "scripts", "sample_recent_activity.json")
START = "<!-- dynamic:recent-activity:start -->"
END = "<!-- dynamic:recent-activity:end -->"
HEADING = "### 🛰️ Recent Signal Telemetry"
MAX_EVENTS = 5
HEADERS = {
    "User-Agent": "recent-activity-bot/1.0",
    "Accept": "application/vnd.github+json",
}

_token = os.getenv("GITHUB_TOKEN")
if _token:
    HEADERS["Authorization"] = f"Bearer {_token}"

_pattern = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)

Event = dict[str, object]


def fetch_events_from_api() -> List[Event]:
    url = f"https://api.github.com/users/{USER}/events/public"
    req = request.Request(url, headers=HEADERS)
    with request.urlopen(req, timeout=20) as resp:
        if resp.status >= 400:
            raise error.HTTPError(url, resp.status, resp.reason, resp.headers, None)
        payload = resp.read().decode("utf-8")
    return json.loads(payload)


def load_fallback_events() -> List[Event]:
    if not os.path.exists(FALLBACK_PATH):
        return []
    with open(FALLBACK_PATH, "r", encoding="utf-8") as handle:
        try:
            payload = json.load(handle)
        except json.JSONDecodeError:
            return []
    events = payload if isinstance(payload, list) else []
    return events


def fetch_events() -> List[Event]:
    try:
        return fetch_events_from_api()
    except error.HTTPError as exc:  # pragma: no cover
        print(f"[recent-activity] HTTP error: {exc}", file=sys.stderr)
    except error.URLError as exc:  # pragma: no cover
        print(f"[recent-activity] Network error: {exc}", file=sys.stderr)

    fallback = load_fallback_events()
    if fallback:
        print("[recent-activity] Using fallback telemetry cache", file=sys.stderr)
    return fallback


def humanize_timestamp(value: str) -> str:
    if not value:
        return ""
    try:
        stamp = dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return value.replace("T", " ").replace("Z", " UTC")

    now = dt.datetime.now(dt.timezone.utc)
    delta = now - stamp
    seconds = max(int(delta.total_seconds()), 0)

    if seconds < 60:
        relative = f"{seconds}s ago"
    elif seconds < 3600:
        relative = f"{seconds // 60}m ago"
    elif seconds < 86400:
        relative = f"{seconds // 3600}h ago"
    else:
        relative = f"{delta.days}d ago"

    return f"{stamp:%Y-%m-%d %H:%M UTC} ({relative})"


def describe_event(event: Event) -> Tuple[str, str, str]:
    etype = event.get("type", "Event")
    repo = event.get("repo", {}).get("name", "unknown/unknown")
    base_url = f"https://github.com/{repo}"
    raw_payload = event.get("payload")
    payload = raw_payload if isinstance(raw_payload, dict) else {}

    icon = "✨"
    message = etype.replace("Event", " activity") or "activity"
    detail_url = base_url

    if etype == "PushEvent":
        commits = payload.get("commits", [])
        if commits:
            message = commits[-1].get("message", "push update")
        else:
            message = "push update"
        detail_url = f"{base_url}/commits"
        icon = "🚀"
    elif etype == "PullRequestEvent":
        pr = payload.get("pull_request", {})
        number = pr.get("number") or payload.get("number")
        detail_url = pr.get("html_url", base_url)
        action = payload.get("action", "updated")
        message = f"PR #{number} {action}"
        icon = "📦"
    elif etype == "IssuesEvent":
        issue = payload.get("issue", {})
        number = issue.get("number")
        detail_url = issue.get("html_url", base_url)
        action = payload.get("action", "updated")
        message = f"Issue #{number} {action}"
        icon = "🛠️"
    elif etype == "IssueCommentEvent":
        issue = payload.get("issue", {})
        number = issue.get("number")
        detail_url = issue.get("html_url", base_url)
        message = f"Commented on issue #{number}"
        icon = "💬"
    elif etype == "PullRequestReviewEvent":
        pr = payload.get("pull_request", {})
        number = pr.get("number")
        detail_url = pr.get("html_url", base_url)
        message = f"Reviewed PR #{number}"
        icon = "🧪"
    elif etype == "ReleaseEvent":
        release = payload.get("release", {})
        tag = release.get("tag_name", "draft")
        detail_url = release.get("html_url", base_url)
        action = payload.get("action", "published")
        message = f"Release {tag} {action}"
        icon = "🎉"
    elif etype == "CreateEvent":
        ref_type = payload.get("ref_type", "resource")
        ref = payload.get("ref", "")
        message = f"Created {ref_type} {ref}".strip()
        icon = "🆕"
    elif etype == "ForkEvent":
        forkee = payload.get("forkee", {})
        fork_name = forkee.get("full_name", "new fork")
        detail_url = forkee.get("html_url", detail_url)
        message = f"Forked to {fork_name}"
        icon = "🌱"
    elif etype == "WatchEvent":
        action = payload.get("action", "starred")
        message = f"{action.title()} {repo}"
        icon = "⭐"

    return icon, message, detail_url


def format_event(event: Event) -> str:
    repo = event.get("repo", {}).get("name", "unknown/unknown")
    icon, message, detail_url = describe_event(event)
    created_human = humanize_timestamp(str(event.get("created_at", "")))
    stamp = f" · {created_human}" if created_human else ""
    return f"- {icon} [{repo}]({detail_url}) · {message}{stamp}".strip()


def unique_events(events: List[Event]) -> List[Event]:
    seen: Set[str] = set()
    unique: List[Event] = []
    for event in events:
        event_id = str(event.get("id"))
        if event_id in seen:
            continue
        seen.add(event_id)
        unique.append(event)
    return unique


def render_activity(events: List[Event]) -> str:
    if not events:
        return "_No public signals detected in the last window._"
    sanitized = unique_events(events)
    if not sanitized:
        return "_No public signals detected in the last window._"
    lines = [format_event(event) for event in sanitized[:MAX_EVENTS]]
    return "\n".join(lines)


def build_block(body: str, stamp: str) -> str:
    lines = [
        START,
        HEADING,
        body,
        f"<sub>{stamp}</sub>",
        END,
    ]
    return "\n".join(lines)


def update_readme(content: str) -> str:
    events = fetch_events()
    body = render_activity(events)
    stamp = dt.datetime.utcnow().strftime("Last sync: %Y-%m-%d %H:%M UTC")
    block = build_block(body, stamp)

    if not _pattern.search(content):
        raise ValueError("Dynamic markers not found in README")

    return _pattern.sub(block, content)


def main() -> None:
    with open(README_PATH, "r", encoding="utf-8") as handle:
        original = handle.read()

    updated = update_readme(original)

    if updated != original:
        with open(README_PATH, "w", encoding="utf-8") as handle:
            handle.write(updated + "\n")


if __name__ == "__main__":
    main()
