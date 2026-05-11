#!/usr/bin/env python3
"""
Deterministic GitHub repository telemetry collector.

Reads:
  - identity/repos.json

Writes:
  - metrics/metrics.json
  - metrics/aggregate.json

Rules:
  - Deterministic output order.
  - No secrets written to disk.
  - Uses GITHUB_TOKEN only if present.
  - Fails softly per repo if GitHub API is unavailable.
  - Does not mutate README directly.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
IDENTITY_REPOS = ROOT / "identity" / "repos.json"
METRICS_DIR = ROOT / "metrics"
METRICS_JSON = METRICS_DIR / "metrics.json"
AGGREGATE_JSON = METRICS_DIR / "aggregate.json"

DEFAULT_OWNER = "popdeuxrem"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path}: {exc}") from exc


def write_json(path: Path, payload: Any, dry_run: bool = False) -> None:
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

    if dry_run:
        print(f"DRY-RUN: would write {path.relative_to(ROOT)}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(encoded, encoding="utf-8")
    print(f"WROTE: {path.relative_to(ROOT)}")


def normalize_repo_item(item: Any) -> dict[str, str]:
    if isinstance(item, str):
        value = item.strip()
        if "/" in value:
            owner, name = value.split("/", 1)
        else:
            owner, name = DEFAULT_OWNER, value

        return {
            "owner": owner.strip(),
            "name": name.strip(),
            "full_name": f"{owner.strip()}/{name.strip()}",
        }

    if isinstance(item, dict):
        full_name = (
            item.get("full_name")
            or item.get("repo")
            or item.get("slug")
            or item.get("name")
            or ""
        )

        full_name = str(full_name).strip()

        if "/" in full_name:
            owner, name = full_name.split("/", 1)
        else:
            owner = str(item.get("owner") or DEFAULT_OWNER).strip()
            name = full_name

        return {
            "owner": owner,
            "name": name,
            "full_name": f"{owner}/{name}",
        }

    return {
        "owner": DEFAULT_OWNER,
        "name": "unknown",
        "full_name": f"{DEFAULT_OWNER}/unknown",
    }


def load_repo_registry() -> list[dict[str, str]]:
    raw = load_json(IDENTITY_REPOS, [])

    if isinstance(raw, dict):
        candidates = raw.get("repos") or raw.get("repositories") or []
    else:
        candidates = raw

    repos: list[dict[str, str]] = []

    if isinstance(candidates, list):
        for item in candidates:
            repo = normalize_repo_item(item)
            if repo["name"] and repo["name"] != "unknown":
                repos.append(repo)

    deduped: dict[str, dict[str, str]] = {}
    for repo in repos:
        deduped[repo["full_name"].lower()] = repo

    return [deduped[key] for key in sorted(deduped.keys())]


def github_request(path: str, token: str | None, timeout: int = 15) -> tuple[int, dict[str, Any] | None, str | None]:
    url = f"https://api.github.com{path}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "popdeuxrem-surface-telemetry",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = int(response.status)
            body = response.read().decode("utf-8")
            return status, json.loads(body), None
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        return int(exc.code), None, error_body[:500]
    except Exception as exc:
        return 0, None, str(exc)


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def collect_repo(repo: dict[str, str], token: str | None, offline: bool = False) -> dict[str, Any]:
    full_name = repo["full_name"]
    owner = repo["owner"]
    name = repo["name"]

    base = {
        "full_name": full_name,
        "owner": owner,
        "name": name,
        "html_url": f"https://github.com/{full_name}",
        "status": "unavailable",
        "description": None,
        "language": None,
        "stars": 0,
        "forks": 0,
        "watchers": 0,
        "open_issues": 0,
        "default_branch": None,
        "archived": False,
        "disabled": False,
        "private": False,
        "pushed_at": None,
        "updated_at": None,
        "collected_at": utc_now(),
        "error": None,
    }

    if offline:
        base["status"] = "offline"
        base["error"] = "offline mode enabled"
        return base

    status, payload, error = github_request(f"/repos/{full_name}", token)

    if status == 200 and isinstance(payload, dict):
        base.update(
            {
                "status": "tracked",
                "description": payload.get("description"),
                "language": payload.get("language"),
                "stars": safe_int(payload.get("stargazers_count")),
                "forks": safe_int(payload.get("forks_count")),
                "watchers": safe_int(payload.get("watchers_count")),
                "open_issues": safe_int(payload.get("open_issues_count")),
                "default_branch": payload.get("default_branch"),
                "archived": bool(payload.get("archived")),
                "disabled": bool(payload.get("disabled")),
                "private": bool(payload.get("private")),
                "pushed_at": payload.get("pushed_at"),
                "updated_at": payload.get("updated_at"),
                "html_url": payload.get("html_url") or base["html_url"],
                "error": None,
            }
        )
        return base

    base["status"] = "unavailable"
    base["error"] = f"GitHub API status={status}; {error or 'unknown error'}"
    return base


def aggregate_metrics(repos: list[dict[str, Any]]) -> dict[str, Any]:
    tracked = [repo for repo in repos if repo.get("status") == "tracked"]

    languages: dict[str, int] = {}
    for repo in tracked:
        language = repo.get("language") or "Unknown"
        languages[language] = languages.get(language, 0) + 1

    top_repos = sorted(
        tracked,
        key=lambda item: (
            -safe_int(item.get("stars")),
            str(item.get("full_name", "")).lower(),
        ),
    )[:8]

    return {
        "generated_at": utc_now(),
        "source": "scripts/collect_repo_metrics.py",
        "registry": "identity/repos.json",
        "repo_count": len(repos),
        "tracked_count": len(tracked),
        "unavailable_count": len(repos) - len(tracked),
        "total_stars": sum(safe_int(repo.get("stars")) for repo in tracked),
        "total_forks": sum(safe_int(repo.get("forks")) for repo in tracked),
        "total_open_issues": sum(safe_int(repo.get("open_issues")) for repo in tracked),
        "languages": dict(sorted(languages.items(), key=lambda item: item[0].lower())),
        "top_repos": [
            {
                "full_name": repo.get("full_name"),
                "name": repo.get("name"),
                "html_url": repo.get("html_url"),
                "stars": safe_int(repo.get("stars")),
                "forks": safe_int(repo.get("forks")),
                "language": repo.get("language"),
                "status": repo.get("status"),
            }
            for repo in top_repos
        ],
    }


def build_metrics_payload(repos: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "generated_at": utc_now(),
        "source": "scripts/collect_repo_metrics.py",
        "registry": "identity/repos.json",
        "repositories": repos,
        "repos": repos,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="print planned writes without mutating files")
    parser.add_argument("--offline", action="store_true", help="do not call GitHub API; write offline telemetry shape")
    parser.add_argument("--sleep", type=float, default=0.2, help="sleep between GitHub API calls")
    args = parser.parse_args()

    repos = load_repo_registry()

    if not repos:
        print("WARN: no repositories found in identity/repos.json", file=sys.stderr)

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    collected: list[dict[str, Any]] = []

    for repo in repos:
        result = collect_repo(repo, token=token, offline=args.offline)
        collected.append(result)

        if args.sleep > 0 and not args.offline:
            time.sleep(args.sleep)

    collected = sorted(collected, key=lambda item: str(item.get("full_name", "")).lower())

    metrics_payload = build_metrics_payload(collected)
    aggregate_payload = aggregate_metrics(collected)

    write_json(METRICS_JSON, metrics_payload, dry_run=args.dry_run)
    write_json(AGGREGATE_JSON, aggregate_payload, dry_run=args.dry_run)

    print(
        "SUMMARY: repos={} tracked={} unavailable={}".format(
            aggregate_payload["repo_count"],
            aggregate_payload["tracked_count"],
            aggregate_payload["unavailable_count"],
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
