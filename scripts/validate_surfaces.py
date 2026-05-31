#!/usr/bin/env python3
"""
Surface validation script.
Validates SVG XML, HTML structure, JSON schemas.
"""
from __future__ import annotations
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SVG_ASSETS = [
    "assets/system-health.svg",
    "assets/workflow-status.svg",
    "assets/repo-metrics.svg",
    "assets/system-matrix.svg",
    "assets/flow-line.svg",
    "assets/section_quote.svg",
]

JSON_SCHEMAS = [
    "data/projects.json",
    "metrics/github_telemetry.json",
    "portfolio.json",
    "health/system_health.json",
]


def validate_svg(path: Path) -> bool:
    try:
        ET.parse(path)
        return True
    except ET.ParseError as e:
        print(f"INVALID SVG: {path} - {e}")
        return False


def validate_json(path: Path) -> bool:
    try:
        with open(path, encoding="utf-8") as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        print(f"INVALID JSON: {path} - {e}")
        return False


def validate_html(path: Path) -> bool:
    try:
        content = path.read_text(encoding="utf-8")
        # Basic structure check
        if "<!DOCTYPE html>" not in content:
            print(f"MISSING DOCTYPE: {path}")
            return False
        if "</html>" not in content:
            print(f"MISSING CLOSING TAG: {path}")
            return False
        return True
    except Exception as e:
        print(f"INVALID HTML: {path} - {e}")
        return False


def main() -> int:
    errors = []

    # Validate SVGs
    for svg in SVG_ASSETS:
        path = ROOT / svg
        if not path.exists():
            errors.append(f"MISSING: {svg}")
        elif not validate_svg(path):
            errors.append(f"SVG FAIL: {svg}")

    # Validate JSON schemas
    for js in JSON_SCHEMAS:
        path = ROOT / js
        if path.exists() and not validate_json(path):
            errors.append(f"JSON FAIL: {js}")

    # Validate index.html
    index_path = ROOT / "index.html"
    if not index_path.exists():
        errors.append("MISSING: index.html")
    elif not validate_html(index_path):
        errors.append("HTML FAIL: index.html")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print("VALIDATION PASS: All surfaces valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())