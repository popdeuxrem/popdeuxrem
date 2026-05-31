# Surface Engine Changelog

## v15.0
### Added
- Canonical `data/projects.json` schema for unified project metadata
- `scripts/fetch_github_telemetry.py` for deterministic GitHub API ingestion
- `scripts/generate_pages_surface.py` for hydrated GitHub Pages surface
- `scripts/validate_surfaces.py` for multi-layer validation
- `SURFACE_ENGINE.md` architecture documentation

### Changed
- All SVG generation uses unified `svg_panel_shell()` primitive
- README generation reads from canonical `data/projects.json`
- Mobile layout uses vertical stacked panels (no HTML tables)

### Fixed
- workflow-status.svg malformed XML filter structure
- Missing `</filter>` closing tag in SVG generation

### Removed
- Internal telemetry sections from public README
- Operating Position, Health Contract, Build Attestation sections

## v14.1
### Added
- GitHub Pages glassmorphism surface (index.html)
- Mobile-responsive CSS grid layout
- Staggered card animations

### Changed
- Fixed workflow-status.svg XML validation error
- Unified table layout to mobile-safe structure

## v14.0
### Added
- Initial Live Surface Console implementation
- SVG telemetry panels
- Deterministic generation pipeline
- AUTO-GENERATED sentinel markers