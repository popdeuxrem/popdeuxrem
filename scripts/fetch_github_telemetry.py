#!/usr/bin/env python3
"""
Deterministic GitHub telemetry ingestion.
Uses only stdlib. No external dependencies.
Support GITHUB_TOKEN if available, degrades gracefully.
"""
from __future__ import annotations
import hashlib
import json
import os
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_JSON = ROOT / "data" / "projects.json"
METRICS_JSON = ROOT / "metrics" / "github_telemetry.json"
CACHE_TTL_SECONDS = 3600


def load_projects() -> list[dict[str, Any]]:
    if not PROJECTS_JSON.exists():
        return []
    return json.loads(PROJECTS_JSON.read_text(encoding="utf-8")).get("projects", [])


def fetch_repo_data(repo: str, token: str | None = None) -> dict[str, Any]:
    """Fetch repository data from GitHub API."""
    api_url = f"https://api.github.com/repos/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        return {}


def fetch_workflow_runs(repo: str, token: str | None = None) -> dict[str, Any]:
    """Fetch workflow run data from GitHub API."""
    api_url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=5"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        return {}


def normalize_repo_name(full_name: str) -> str:
    """Extract owner/repo from full_name or return as-is if already formatted."""
    if "/" in full_name:
        return full_name
    return f"popdeuxrem/{full_name}"


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    projects = load_projects()
    telemetry: list[dict[str, Any]] = []

    for project in projects:
        repo_full = project.get("repo", "")
        if not repo_full:
            continue

        # Extract owner/repo from URL
        repo = repo_full.replace("https://github.com/", "").replace("github.com/", "")

        repo_data = fetch_repo_data(repo, token) if token or True else {}

        workflow_data = fetch_workflow_runs(repo, token) if token else {}

        # Get latest workflow status if available
        workflow_status = "UNKNOWN"
        latest_run = {}
        if isinstance(workflow_data.get("workflow_runs"), list) and workflow_data["workflow_runs"]:
            run = workflow_data["workflow_runs"][0]
            latest_run = {
                "conclusion": run.get("conclusion", "unknown"),
                "status": run.get("status", "unknown"),
                "created_at": run.get("created_at", ""),
            }
            workflow_status = run.get("status", "unknown").upper()

        normalized = {
            "id": project.get("id"),
            "name": project.get("name"),
            "stars": repo_data.get("stargazers_count", project.get("stars", 0)),
            "forks": repo_data.get("forks_count", 0),
            "open_issues": repo_data.get("open_issues_count", 0),
            "updated_at": repo_data.get("updated_at", ""),
            "workflow_status": workflow_status,
            "latest_run": latest_run,
        }
        telemetry.append(normalized)

    # Sort alphabetically by id for deterministic output
    telemetry = sorted(telemetry, key=lambda x: str(x.get("id", "")).lower())

    payload = {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cache_ttl_seconds": CACHE_TTL_SECONDS,
        "source": "github_api",
        "token_used": bool(token),
        "projects": telemetry,
    }

    METRICS_JSON.parent.mkdir(parents=True, exist_ok=True)
    METRICS_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {METRICS_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())