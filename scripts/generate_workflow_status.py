#!/usr/bin/env python3
"""
Deterministic workflow status SVG generator.
Reads:
  - .github/workflows/readme-sync.yml
  - dist/build-manifest.json
  - health/system_health.json
  - telemetry/workflows.json
Writes:
  - assets/workflow-status.svg
Rules:
  - no network calls
  - deterministic SVG structure
  - safe fallback if telemetry is missing
  - no secrets
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "readme-sync.yml"
MANIFEST = ROOT / "dist" / "build-manifest.json"
HEALTH = ROOT / "health" / "system_health.json"
TELEMETRY = ROOT / "telemetry" / "workflows.json"
OUT = ROOT / "assets" / "workflow-status.svg"
def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)
def read_text(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return default
def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default
def file_status(path: Path) -> str:
    return "present" if path.exists() else "missing"
def bool_status(condition: bool) -> str:
    return "ok" if condition else "missing"
def color_for(status: str) -> str:
    normalized = str(status or "").lower()
    if normalized in {"ok", "present", "healthy", "success", "completed", "passing"}:
        return "#00ff9d"
    if normalized in {"watch", "warning", "degraded", "queued", "in_progress", "neutral", "skipped"}:
        return "#d29922"
    if normalized in {"missing", "failed", "failure", "error", "critical", "cancelled", "timed_out", "action_required"}:
        return "#ff5c8a"
    if normalized in {"unavailable", "unknown", "none"}:
        return "#8b949e"
    return "#8b949e"
def workflow_contract() -> dict[str, str]:
    text = read_text(WORKFLOW)
    return {
        "workflow_file": file_status(WORKFLOW),
        "manual_dispatch": bool_status("workflow_dispatch:" in text),
        "scheduled_sync": bool_status("schedule:" in text and "cron:" in text),
        "explicit_permissions": bool_status("permissions:" in text and "contents: write" in text),
        "concurrency": bool_status("concurrency:" in text),
        "no_broad_git_add": bool_status("git add ." not in text),
        "validation_gate": bool_status("make validate" in text),
        "build_gate": bool_status("make build" in text),
    }
def build_context() -> dict[str, str]:
    manifest = load_json(MANIFEST, {})
    health = load_json(HEALTH, {})
    source_hash = "unknown"
    generator = "unknown"
    if isinstance(manifest, dict):
        source_hash = str(manifest.get("short_sha") or manifest.get("source_hash") or "unknown")[:16]
        generator = str(manifest.get("generator", "unknown"))
    health_status = "unknown"
    if isinstance(health, dict):
        health_status = str(health.get("status", "unknown"))
    return {
        "manifest": file_status(MANIFEST),
        "health": health_status,
        "source_hash": source_hash,
        "generator": generator,
    }
def workflow_telemetry() -> dict[str, str]:
    payload = load_json(TELEMETRY, {})
    if not isinstance(payload, dict):
        return {
            "telemetry": "missing",
            "collector": "missing",
            "latest": "unavailable",
            "conclusion": "none",
            "workflow": "unknown",
            "branch": "unknown",
            "sha": "unknown",
            "runs": "0",
        }
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    return {
        "telemetry": file_status(TELEMETRY),
        "collector": str(payload.get("collector_status") or "unknown"),
        "latest": str(summary.get("latest_status") or "unavailable"),
        "conclusion": str(summary.get("latest_conclusion") or "none"),
        "workflow": str(summary.get("latest_workflow") or "unknown")[:28],
        "branch": str(summary.get("latest_branch") or "unknown")[:24],
        "sha": str(summary.get("latest_sha") or "unknown")[:12],
        "runs": str(summary.get("run_count") or 0),
    }
def overall_status(contract: dict[str, str], context: dict[str, str], telemetry: dict[str, str]) -> str:
    contract_values = list(contract.values()) + [context.get("manifest", "missing")]
    if any(value == "missing" for value in contract_values):
        return "degraded"
    conclusion = telemetry.get("conclusion", "none").lower()
    latest = telemetry.get("latest", "unavailable").lower()
    health = context.get("health", "unknown").lower()
    if conclusion in {"failure", "failed", "cancelled", "timed_out", "action_required"}:
        return "failed"
    if latest in {"queued", "in_progress"}:
        return "watch"
    if telemetry.get("collector") == "unavailable":
        return "watch"
    if health in {"watch", "degraded", "unknown"}:
        return "watch"
    return "healthy"
def svg(contract: dict[str, str], context: dict[str, str], telemetry: dict[str, str]) -> str:
    status = overall_status(contract, context, telemetry)
    trace_seed = json.dumps({"contract": contract, "context": context, "telemetry": telemetry}, sort_keys=True)
    trace = hashlib.sha256(trace_seed.encode("utf-8")).hexdigest()[:12]
    rows = [
        ("WORKFLOW", contract["workflow_file"]),
        ("DISPATCH", contract["manual_dispatch"]),
        ("SCHEDULE", contract["scheduled_sync"]),
        ("PERMISSIONS", contract["explicit_permissions"]),
        ("CONCURRENCY", contract["concurrency"]),
        ("VALIDATE", contract["validation_gate"]),
        ("MANIFEST", context["manifest"]),
        ("HEALTH", context["health"]),
        ("TELEMETRY", telemetry["telemetry"]),
        ("COLLECTOR", telemetry["collector"]),
        ("LATEST", telemetry["latest"]),
        ("RESULT", telemetry["conclusion"]),
        ("RUNS", telemetry["runs"]),
    ]
    row_svg = []
    y = 70
    for label, value in rows:
        color = color_for(value)
        row_svg.append(
            '<text x="44" y="{y}" fill="#8b949e" font-family="monospace" font-size="12">{label}</text>'
            '<circle cx="250" cy="{dot_y}" r="5" fill="{color}"/>'
            '<text x="268" y="{y}" fill="{color}" font-family="monospace" font-size="12">{value}</text>'.format(
                y=y,
                dot_y=y - 4,
                color=color,
                label=esc(label),
                value=esc(str(value).upper()[:26]),
            )
        )
        y += 23
    overall_color = color_for(status)
    return '''<svg width="560" height="430" viewBox="0 0 560 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Workflow status panel">
  <defs>
    <linearGradient id="border" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#00f3ff"/>
      <stop offset="50%" stop-color="#bc8cff"/>
      <stop offset="100%" stop-color="#00ff9d"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </defs>
  <rect width="560" height="430" rx="18" fill="#0d1117"/>
  <rect x="1" y="1" width="558" height="428" rx="18" fill="none" stroke="url(#border)" stroke-width="1.5" opacity="0.78"/>
  <text x="44" y="36" fill="#00f3ff" font-family="monospace" font-size="14" font-weight="700">WORKFLOW CONTROL</text>
  <circle cx="490" cy="31" r="7" fill="{overall_color}" filter="url(#glow)"/>
  {rows}
  <text x="44" y="382" fill="#8b949e" font-family="monospace" font-size="10">workflow:{workflow} · branch:{branch} · sha:{sha}</text>
  <text x="44" y="404" fill="#484f58" font-family="monospace" font-size="10">trace:{trace} · source:{source_hash}</text>
</svg>
'''.format(
        rows="\n  ".join(row_svg),
        overall_color=overall_color,
        workflow=esc(telemetry.get("workflow", "unknown")),
        branch=esc(telemetry.get("branch", "unknown")),
        sha=esc(telemetry.get("sha", "unknown")),
        trace=esc(trace),
        source_hash=esc(context.get("source_hash", "unknown")),
    )
def write_output(content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"DRY-RUN: would write {OUT.relative_to(ROOT)}")
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    contract = workflow_contract()
    context = build_context()
    telemetry = workflow_telemetry()
    write_output(svg(contract, context, telemetry), dry_run=args.dry_run)
    print("SUMMARY: workflow_status={}".format(overall_status(contract, context, telemetry)))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
