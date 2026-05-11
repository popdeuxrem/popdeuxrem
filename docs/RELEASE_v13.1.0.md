# Release v13.1.0

## Release Name

v13.1.0 — Manifest-Aware Project Surface

---

## Objective

Extend the deterministic GitHub Surface Engine so the generated build manifest records the project-card index and card inventory.

This release strengthens traceability between:

    metrics/metrics.json
      -> scripts/generate_project_cards.py
      -> assets/projects/index.json
      -> assets/projects/*.svg
      -> scripts/build_readme.py
      -> dist/build-manifest.json
      -> README.md

---

## Added

- Project-card manifest inventory in `dist/build-manifest.json`.
- `project_cards_index` manifest field.
- `project_cards_count` manifest field.
- `project_cards` manifest field.
- Release note for `v13.1.0`.

---

## Changed

- `scripts/build_readme.py` now records generated project-card state in `dist/build-manifest.json`.
- `dist/build-manifest.json` now provides stronger attestation for generated project card assets.

---

## Validation Contract

Run:

    python3 -m py_compile scripts/build_readme.py
    python3 scripts/generate_project_cards.py --limit 8
    python3 scripts/generate_workflow_status.py
    python3 scripts/build_readme.py
    python3 -m json.tool dist/build-manifest.json >/dev/null
    make validate

Expected manifest fields:

    project_cards_index
    project_cards_count
    project_cards

---

## Release Gate

Before tagging:

    git status --short --branch
    make validate
    git diff --cached --name-status

The tag may be created only if:

- Working tree changes are intentional.
- `make validate` passes.
- `dist/build-manifest.json` is valid JSON.
- Manifest includes project-card fields.
- README renders project cards.
- No local-only files are staged.

---

## Tag

    v13.1.0

---

## Rollback

If the release breaks manifest generation:

    git revert <release_commit_sha>
    make validate
    git push origin main

If the tag was pushed and must be removed:

    git tag -d v13.1.0
    git push origin :refs/tags/v13.1.0
