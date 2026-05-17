# Changelog

## v13.2.0 — Workflow Telemetry Surface

Added

* Added live GitHub Actions workflow telemetry ingestion.
* Added telemetry/workflows.json as the run-state source for workflow panels.
* Added telemetry-aware workflow status SVG rendering.
* Added workflow telemetry documentation.

Changed

* Updated scripts/generate_workflow_status.py to read local telemetry state.
* Updated README surface artifacts with workflow telemetry rendering.
* Preserved the network boundary: telemetry collection is separate from README generation.

Validation

* make validate passes.
* Offline telemetry fallback path is supported.
* Live telemetry collection succeeds when gh or GitHub API access is available.

This repo follows an operational release model:
```txt
plan -> patch -> validate -> diff -> commit -> push -> observe -> rollback

⸻

[v13.0.0] - 2026-05-11

Summary

v13.0.0 stabilizes the repository into a deterministic GitHub profile surface engine.

The project now has one canonical README path, one validation gate, generated operational SVG panels, a build manifest, hardened GitHub Actions, and a documented rollback posture.

⸻

Added

* Canonical deterministic README surface engine.
* README.base.md as the source-of-truth README template.
* README.md as generated output.
* dist/build-manifest.json for build attestation.
* Generated operational SVG panels:
    * assets/system-health.svg
    * assets/repo-metrics.svg
* Final architecture report:
    * docs/FINAL_ARCHITECTURE_REPORT.md
* README surface audit:
    * docs/README_SURFACE_AUDIT.md
* Targeted README evolution utility:
    * tools/evolve_readme_base.py
* Hardened GitHub Actions workflow:
    * .github/workflows/readme-sync.yml
* Local validation contract through:
    * make validate
    * make build
    * make dry-run
    * make health
    * make status

⸻

Changed

* Rebuilt scripts/build_readme.py as the canonical deterministic generator.
* Hardened scripts/quantum_build.sh into a defensive build and validation gate.
* Strengthened Makefile into the primary operational interface.
* Updated systems/scripts/system_health.sh for standalone-safe execution.
* Updated systems/intelligence/render_status.sh to consume normalized health status.
* Evolved the README surface from v12.0 to v13.0 while preserving the existing quantum identity language.
* Updated workflow behavior so generated outputs are committed through an explicit allowlist.

⸻

Fixed

* Removed split-brain README generation architecture.
* Removed the competing .github/workflows/update-readme.yml workflow.
* Removed broad git add . behavior from GitHub Actions.
* Fixed false JSON path validation warnings.
* Fixed dependency import-name checks.
* Fixed dry-run side effects in README generation.
* Fixed brittle README timestamp/hash replacement behavior.
* Fixed health schema mismatch between system health generation and status rendering.
* Fixed standalone log-directory failure in health generation.
* Fixed workflow collision risk by adding concurrency control.

⸻

Security

* GitHub Actions now uses explicit generated-output staging.
* Workflow permissions are explicitly scoped to contents: write.
* Workflow concurrency prevents overlapping README surface sync runs.
* Local backup and rollback path were established before mutation.
* Local-only files are ignored:
    * .backups/
    * docs/STEP_*_OUTPUT.txt

⸻

Validation

Passed locally:

make validate
make build
python3 scripts/build_readme.py --dry-run --check

Validation contract:

python syntax       : pass
bash syntax         : pass
json syntax         : pass
template markers    : pass
generator dry-run   : pass
system health       : pass
status renderer     : pass
quantum build check : pass

⸻

Final Pushed Commit

9fd3f27 feat: stabilize deterministic README surface engine

⸻

[v12.0.0] - Previous

Existing Surface

* Quantum profile README surface.
* Generated SVG identity assets.
* Profile telemetry files.
* README automation scripts.
* Scheduled README sync workflows.

⸻

Deprecated

* removed legacy tmp README artifact as README source of truth.
* Competing README workflow architecture.
* Broad workflow staging through git add ..

⸻

Release Contract

Every release must preserve this architecture:

README.base.md
  -> scripts/build_readme.py
  -> README.md + generated assets + dist/build-manifest.json
  -> make validate
  -> GitHub Actions sync

A release is valid only when:

[ ] make validate passes
[ ] make build passes
[ ] README renders correctly
[ ] generated assets exist
[ ] build manifest is valid JSON
[ ] workflow has no git add .
[ ] split-brain workflow is absent
[ ] diff is reviewed
[ ] no secrets are staged
[ ] rollback path is known

