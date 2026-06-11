# Lysergic Surface Engine v15.0

## Architecture Overview

The Surface Engine is a deterministic, telemetry-driven identity platform that generates:
- GitHub README.md (generated content block)
- GitHub Pages index.html
- SVG telemetry panels

## Generator Contracts

### Canonical Sources
- `README.base.md` - Human-authored template
- `data/projects.json` - Canonical project metadata
- `health/*.json` - System health state
- `metrics/github_telemetry.json` - GitHub API telemetry

### Output Artifacts
- `README.md` - Generated README (only auto-generated section)
- `index.html` - GitHub Pages surface
- `assets/*.svg` - Deterministic SVG panels

## Deterministic Guarantees

All outputs are:
- Reproducible from source JSON
- Stable across rebuilds
- Hashed from canonical inputs
- Idempotent generation

## Rendering Pipeline

### SVG Generation
All SVG panels use unified `svg_panel_shell()` primitive:
- Consistent gradients (#00f3ff → #bc8cff → #00ff9d)
- Glow filter (stdDeviation=3)
- 16px border radius
- Dark theme (#0d1117 background)

### Status Colors
- SHIP: green (#4ade80)
- BUILD: amber (#f59e0b)
- DESIGN: purple (#a855f7)
- ARCHIVE: slate (#94a3b8)
- EXPERIMENTAL: cyan (#22d3ee)

## Deployment Model

GitHub Actions workflow triggers on:
- Push to main
- Scheduled daily
- Manual dispatch

## Rollback Strategy

All generated artifacts are:
- Version-controlled
- Hash-verified
- Reversible via git