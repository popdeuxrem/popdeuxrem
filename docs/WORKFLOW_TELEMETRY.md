# Workflow Telemetry
## Purpose
Workflow telemetry makes the GitHub profile surface aware of recent GitHub Actions run state without allowing README generation to call the network.
The network boundary is isolated to:
```txt
scripts/collect_workflow_runs.py

The render path remains local and deterministic:

telemetry/workflows.json
  -> scripts/generate_workflow_status.py
  -> assets/workflow-status.svg
  -> scripts/build_readme.py
  -> README.md

Commands

Collect live workflow run state:

python3 scripts/collect_workflow_runs.py

Collect fallback/offline telemetry shape:

python3 scripts/collect_workflow_runs.py --offline

Regenerate the workflow panel:

python3 scripts/generate_workflow_status.py

Regenerate README:

python3 scripts/build_readme.py

Validate:

make validate

Security Boundary

The collector may use:

GITHUB_TOKEN
GH_TOKEN
gh CLI authenticated state

No token or secret is written to disk.

The telemetry file contains only workflow run metadata:

workflow name
status
conclusion
branch
short SHA
event
run URL
timestamps

Failure Behavior

If GitHub API or gh is unavailable, the collector writes a valid fallback shape:

{
  "collector_status": "unavailable",
  "runs": []
}

The README and SVG generation continue to work.

Release Rule

Network collection must remain outside scripts/build_readme.py.

README generation must stay deterministic and local-only.
