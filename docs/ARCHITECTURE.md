# Quantum Surface v3.0 | Architectural Blueprint

## 1. System Overview
The Quantum Surface is a self-hydrating, bio-digital profile engine. It transforms raw GitHub metadata and local configuration files into a high-fidelity, animated visual interface.

## 2. Core Execution Lifecycle
The system follows a synchronous build-and-inject pattern:
1. **Discovery**: `discovery.py` polls GitHub GraphQL/REST APIs.
2. **Security**: `vuln_scan.sh` performs static analysis on the repo.
3. **Generation**: Sub-generators (`generate_*.py`) create SVG assets in `assets/`.
4. **Hydration**: `update_readme.py` maps data to `config/README.template.md`.
5. **Deployment**: GitHub Actions pushes the reconciled `README.md`.

## 3. Component Manifest
| Component | Script | Output | Function |
| :--- | :--- | :--- | :--- |
| **Header** | `generate_header.py` | `header-plate.svg` | CSS Scan-line animation |
| **Blueprint** | `terminal_shot.sh` | `quantum-terminal.svg`| Automated directory mapping |
| **Waveform** | `generate_waveform.py`| `divider-waveform.svg`| Activity-based pulse frequency |
| **Telemetry** | `generate_telemetry_panel.py` | `telemetry-panel.svg` | Real-time issue/PR counters |
| **Security** | `generate_security_svg.py`| `security-status.svg` | Hygiene & Vulnerability status |

## 4. Data Flow
`config/*.json` ──────┐
                     ▼
`scripts/discovery.py` ──▶ `scripts/update_readme.py` ──▶ `README.md`
                     ▲           │
GitHub API ──────────┘           └─▶ `assets/*.svg`
