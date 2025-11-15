# Animated terminal shells · Usage

This directory contains VHS "tape" definitions and rendered GIFs used in the README.

## Requirements

- [vhs](https://github.com/charmbracelet/vhs)
- Bash
- (Optional) Docker, if you prefer running vhs in a container

## Files

- `quantum-shell-infra.tape` → main infra-focused animated shell (`quantum-shell-animated.gif`).
- `quantum-basilica-shell.tape` → Quantum Basilica / digital garden shell (`quantum-basilica-shell-animated.gif`).
- `../scripts/render_animated_shells.sh` → helper script to render all shells.

## Regenerating locally

From the repo root:

  chmod +x scripts/render_animated_shells.sh
  scripts/render_animated_shells.sh

This overwrites the GIFs in `assets/terminal/` with freshly rendered versions.

You can also render a single tape manually, for example:

  vhs assets/terminal/quantum-shell-infra.tape

## Tweaking the animations

- Edit the `.tape` files to change:
  - commands (infra ops, content flows, etc.),
  - delays (`Sleep`),
  - terminal theme, font size, or dimensions.
- Re-run the render script or invoke `vhs` directly.
- Commit the updated GIFs so they stay in sync with the tapes.

## CI / GitHub Actions

The `.github/workflows/render-animated-shells.yml` workflow renders these GIFs in CI when:

- You trigger it via "Run workflow" (workflow_dispatch), or
- You push changes that touch `assets/terminal/*.tape` or `scripts/render_animated_shells.sh`.

If the rendered GIFs change, the workflow commits and pushes the updated assets back to the repo.
