# Release v13.2.0
## Release Name
`v13.2.0` — Workflow Telemetry Surface
---
## Objective
Promote the live workflow telemetry system to an official release boundary.
This release extends the deterministic GitHub profile surface with GitHub Actions run telemetry while preserving a strict network boundary.
The network-aware collector is isolated to:
```txt
scripts/collect_workflow_runs.py

The README render path remains deterministic and local-only:

telemetry/workflows.json
  -> scripts/generate_workflow_status.py
  -> assets/workflow-status.svg
  -> scripts/build_readme.py
  -> README.md

⸻

Added

* Live GitHub Actions run telemetry collector.
* telemetry/workflows.json as the workflow run-state source.
* Workflow status SVG support for telemetry state.
* Workflow telemetry documentation.
* Makefile helpers for workflow telemetry operations.

⸻

Changed

* assets/workflow-status.svg now represents workflow telemetry as well as static workflow contract checks.
* scripts/generate_workflow_status.py now reads telemetry/workflows.json.
* README surface generation now includes the evolved workflow panel.
* Build manifest and generated surface artifacts were synchronized with telemetry-aware rendering.

⸻

Security Boundary

No secrets are committed.

The collector may read:

GITHUB_TOKEN
GH_TOKEN
gh CLI authenticated state

No token value is written to disk.

The telemetry output contains only workflow metadata:

workflow name
run status
run conclusion
branch
short SHA
event
URL
timestamps

⸻

Failure Behavior

If GitHub API access or gh CLI is unavailable, the collector writes a valid fallback telemetry shape.

Fallback behavior keeps these commands operational:

python3 scripts/generate_workflow_status.py
python3 scripts/build_readme.py
make validate

⸻

Validation Contract

Run:

python3 -m py_compile scripts/collect_workflow_runs.py
python3 -m py_compile scripts/generate_workflow_status.py
python3 scripts/collect_workflow_runs.py --offline
python3 scripts/generate_workflow_status.py
python3 scripts/build_readme.py
python3 -m json.tool telemetry/workflows.json >/dev/null
python3 -m json.tool dist/build-manifest.json >/dev/null
make validate

Expected:

telemetry/workflows.json exists
assets/workflow-status.svg exists
README.md renders workflow-status.svg
make validate passes

⸻

Release Gate

The release may be tagged only when:

[ ] working tree changes are intentional
[ ] telemetry schema is valid
[ ] fallback collector path works
[ ] live collector path succeeds or falls back safely
[ ] README generation is network-free
[ ] make validate passes
[ ] no secrets or local agent state are staged

⸻

Tag

v13.2.0

⸻

Rollback

If telemetry rendering breaks:

git revert <release_commit_sha>
make validate
git push origin main

If the tag must be removed:

git tag -d v13.2.0
git push origin :refs/tags/v13.2.0

