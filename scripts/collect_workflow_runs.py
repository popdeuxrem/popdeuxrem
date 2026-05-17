#!/usr/bin/env python3
"""
Collect GitHub Actions workflow run telemetry.
Reads:
  - .github/workflows/*.yml
  - git remote origin URL
  - optional GITHUB_TOKEN / GH_TOKEN
Writes:
  - telemetry/workflows.json
Rules:
  - deterministic output order
  - no secrets written
  - soft failure if API/gh unavailable
  - README generation remains network-free
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = ROOT / ".github" / "workflows"
OUT = ROOT / "telemetry" / "workflows.json"
def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def run_cmd(args: list[str], timeout: int = 15) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as exc:
        return 1, "", str(exc)
def write_json(path: Path, payload: Any, dry_run: bool = False) -> None:
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if dry_run:
        print(f"DRY-RUN: would write {path.relative_to(ROOT)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(encoded, encoding="utf-8")
    print(f"WROTE: {path.relative_to(ROOT)}")
def workflow_files() -> list[dict[str, str]]:
    files: list[dict[str, str]] = []
    if not WORKFLOWS_DIR.exists():
        return files
    for path in sorted(WORKFLOWS_DIR.glob("*")):
        if path.suffix.lower() not in {".yml", ".yaml"}:
            continue
        files.append(
            {
                "name": path.stem,
                "path": str(path.relative_to(ROOT)),
            }
        )
    return files
def infer_repo_slug() -> str | None:
    rc, stdout, _stderr = run_cmd(["git", "remote", "get-url", "origin"])
    if rc != 0:
        return None
    url = stdout.strip()
    patterns = [
        r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
        r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return f"{match.group('owner')}/{match.group('repo')}"
    return None
def collect_with_gh(limit: int) -> tuple[bool, list[dict[str, Any]], str | None]:
    rc, stdout, stderr = run_cmd(["gh", "run", "list", "--limit", str(limit), "--json", "databaseId,workflowName,displayTitle,status,conclusion,createdAt,updatedAt,event,headBranch,headSha,url"])
    if rc != 0:
        return False, [], stderr.strip() or "gh run list failed"
    try:
        raw = json.loads(stdout)
    except json.JSONDecodeError as exc:
        return False, [], f"gh JSON parse failed: {exc}"
    if not isinstance(raw, list):
        return False, [], "gh returned non-list payload"
    runs: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        runs.append(
            {
                "id": item.get("databaseId"),
                "workflow_name": item.get("workflowName") or "unknown",
                "display_title": item.get("displayTitle") or "",
                "status": item.get("status") or "unknown",
                "conclusion": item.get("conclusion"),
                "event": item.get("event"),
                "branch": item.get("headBranch"),
                "sha": str(item.get("headSha") or "")[:12],
                "created_at": item.get("createdAt"),
                "updated_at": item.get("updatedAt"),
                "url": item.get("url"),
                "source": "gh",
            }
        )
    return True, sorted(runs, key=lambda run: str(run.get("created_at") or ""), reverse=True), None
def github_api_request(path: str, token: str | None, timeout: int) -> tuple[int, dict[str, Any] | None, str | None]:
    url = f"https://api.github.com{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "popdeuxrem-workflow-telemetry",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return int(response.status), json.loads(response.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        return int(exc.code), None, exc.read().decode("utf-8", errors="replace")[:500]
    except Exception as exc:
        return 0, None, str(exc)
def collect_with_api(repo_slug: str, limit: int, timeout: int) -> tuple[bool, list[dict[str, Any]], str | None]:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    status, payload, error = github_api_request(f"/repos/{repo_slug}/actions/runs?per_page={limit}", token, timeout)
    if status != 200 or not isinstance(payload, dict):
        return False, [], f"GitHub API status={status}; {error or 'unknown error'}"
    raw_runs = payload.get("workflow_runs", [])
    if not isinstance(raw_runs, list):
        return False, [], "GitHub API returned invalid workflow_runs payload"
    runs: list[dict[str, Any]] = []
    for item in raw_runs:
        if not isinstance(item, dict):
            continue
        runs.append(
            {
                "id": item.get("id"),
                "workflow_name": item.get("name") or "unknown",
                "display_title": item.get("display_title") or "",
                "status": item.get("status") or "unknown",
                "conclusion": item.get("conclusion"),
                "event": item.get("event"),
                "branch": item.get("head_branch"),
                "sha": str(item.get("head_sha") or "")[:12],
                "created_at": item.get("created_at"),
                "updated_at": item.get("updated_at"),
                "url": item.get("html_url"),
                "source": "api",
            }
        )
    return True, sorted(runs, key=lambda run: str(run.get("created_at") or ""), reverse=True), None
def summarize_runs(runs: list[dict[str, Any]]) -> dict[str, Any]:
    latest = runs[0] if runs else None
    counts: dict[str, int] = {}
    for run in runs:
        key = str(run.get("conclusion") or run.get("status") or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return {
        "run_count": len(runs),
        "latest_status": latest.get("status") if latest else "unavailable",
        "latest_conclusion": latest.get("conclusion") if latest else None,
        "latest_workflow": latest.get("workflow_name") if latest else None,
        "latest_branch": latest.get("branch") if latest else None,
        "latest_sha": latest.get("sha") if latest else None,
        "latest_url": latest.get("url") if latest else None,
        "counts": dict(sorted(counts.items())),
    }
def fallback_payload(repo_slug: str | None, error: str | None) -> dict[str, Any]:
    return {
        "generated_at": utc_now(),
        "source": "scripts/collect_workflow_runs.py",
        "collector_status": "unavailable",
        "repo": repo_slug,
        "error": error or "workflow telemetry unavailable",
        "workflow_files": workflow_files(),
        "summary": {
            "run_count": 0,
            "latest_status": "unavailable",
            "latest_conclusion": None,
            "latest_workflow": None,
            "latest_branch": None,
            "latest_sha": None,
            "latest_url": None,
            "counts": {},
        },
        "runs": [],
    }
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=15)
    args = parser.parse_args()
    repo_slug = infer_repo_slug()
    if args.offline:
        write_json(OUT, fallback_payload(repo_slug, "offline mode enabled"), dry_run=args.dry_run)
        print("SUMMARY: collector_status=offline")
        return 0
    ok, runs, error = collect_with_gh(args.limit)
    source = "gh"
    if not ok:
        source = "api"
        if repo_slug:
            ok, runs, error = collect_with_api(repo_slug, args.limit, args.timeout)
        else:
            error = error or "could not infer GitHub repository slug"
    if not ok:
        payload = fallback_payload(repo_slug, error)
    else:
        payload = {
            "generated_at": utc_now(),
            "source": "scripts/collect_workflow_runs.py",
            "collector_status": "ok",
            "collector_backend": source,
            "repo": repo_slug,
            "error": None,
            "workflow_files": workflow_files(),
            "summary": summarize_runs(runs),
            "runs": runs,
        }
    write_json(OUT, payload, dry_run=args.dry_run)
    print(
        "SUMMARY: collector_status={} runs={}".format(
            payload.get("collector_status"),
            len(payload.get("runs", [])),
        )
    )
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
