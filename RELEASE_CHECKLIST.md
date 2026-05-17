# Release Checklist
This checklist controls safe releases for the PopDeuxRem / Lysergic GitHub Surface Engine.
---
## Release Objective
Every release must preserve the core architecture:
```txt
README.base.md
  -> scripts/build_readme.py
  -> README.md + generated assets + dist/build-manifest.json
  -> make validate
  -> GitHub Actions sync

Release goals:

deterministic output
auditable changes
explicit validation
safe rollback
no broad workflow mutation
no secret exposure

⸻

1. Preflight

Run from the repository root:

pwd
git status --short --branch
git log --oneline -5

Expected:

- current directory is repo root
- branch is main
- working tree changes are understood
- latest commit is known

⸻

2. Backup

Required before medium/high-risk changes.

set -euo pipefail
mkdir -p .backups
BACKUP_DIR=".backups/pre-release-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$BACKUP_DIR"
for path in \
  README.md \
  README.base.md \
  Makefile \
  scripts \
  systems \
  .github/workflows \
  assets \
  data \
  health \
  metrics \
  identity \
  portfolio.json \
  skills.json \
  timeline.json \
  CHANGELOG.md \
  RELEASE_CHECKLIST.md
do
  if [ -e "$path" ]; then
    cp -a "$path" "$BACKUP_DIR/"
    printf 'BACKED UP: %s\n' "$path"
  else
    printf 'MISSING: %s\n' "$path"
  fi
done
printf 'BACKUP_DIR=%s\n' "$BACKUP_DIR"

Expected:

- backup directory created under .backups/
- critical files copied
- rollback path is known before mutation

⸻

3. Validate Before Mutation

make validate
python3 scripts/build_readme.py --dry-run --check

Expected:

[validate] ok
dry-run prints planned writes only
dry-run does not mutate README.md, assets, health, metrics, or dist

⸻

4. Allowed Source-of-Truth Edits

These may be edited intentionally:

README.base.md
portfolio.json
skills.json
timeline.json
data/quotes.json
identity/repos.json
scripts/build_readme.py
scripts/quantum_build.sh
systems/**
.github/workflows/readme-sync.yml
CHANGELOG.md
RELEASE_CHECKLIST.md
docs/*.md

These are generated or deprecated:

README.md                  generated output
assets/flow-line.svg       generated output
assets/section_quote.svg   generated output
assets/system-health.svg   generated output
assets/repo-metrics.svg    generated output
dist/build-manifest.json   generated output
health/system_health.json  generated health state
removed legacy tmp README artifact                    deprecated; not a source of truth

Do not restore removed legacy tmp README artifact as a README generation source.

⸻

5. Generate Outputs

make build

Expected generated outputs:

README.md
assets/flow-line.svg
assets/section_quote.svg
assets/system-health.svg
assets/repo-metrics.svg
dist/build-manifest.json
health/system_health.json

⸻

6. Validate After Generation

make validate
python3 -m json.tool dist/build-manifest.json >/dev/null
python3 -m json.tool health/system_health.json >/dev/null

Expected:

0 validation errors
valid build manifest
valid health state

⸻

7. Review Diff

git status --short --branch
git diff --name-status
git diff --stat

Review full diffs for high-risk files:

git diff -- \
  README.base.md \
  README.md \
  scripts/build_readme.py \
  scripts/quantum_build.sh \
  .github/workflows/readme-sync.yml \
  Makefile

Expected:

- changes match release intent
- generated files changed only because source inputs changed
- workflow diff does not broaden permissions or staging scope

⸻

8. Secret and Local-Only File Gate

Run:

set -euo pipefail
if git status --short | grep -E '^(\?\?|A|M|D).*(\.env|secret|key|pem|credentials|token|service-account)'; then
  echo "FAIL: possible secret or credential file present in git status"
  exit 1
fi
if git status --short | grep -E '^(\?\?|A|M|D)\s+\.backups/'; then
  echo "FAIL: backup directory must not be staged or committed"
  exit 1
fi
if git status --short | grep -E '^(\?\?|A|M|D)\s+docs/STEP_.*_OUTPUT\.txt'; then
  echo "FAIL: step output files must not be committed"
  exit 1
fi
echo "PASS: secret/local-only gate"

Expected:

PASS: secret/local-only gate

⸻

9. Workflow Safety Gate

set -euo pipefail
if grep -R "git add \." .github/workflows 2>/dev/null; then
  echo "FAIL: broad git add found"
  exit 1
fi
if [ -f .github/workflows/update-readme.yml ]; then
  echo "FAIL: split-brain workflow exists"
  exit 1
fi
grep -q "permissions:" .github/workflows/readme-sync.yml
grep -q "contents: write" .github/workflows/readme-sync.yml
grep -q "concurrency:" .github/workflows/readme-sync.yml
echo "PASS: workflow safety gate"

Expected:

PASS: workflow safety gate

⸻

10. Required File Gate

set -euo pipefail
for file in \
  README.base.md \
  README.md \
  Makefile \
  scripts/build_readme.py \
  scripts/quantum_build.sh \
  systems/intelligence/render_status.sh \
  systems/scripts/system_health.sh \
  .github/workflows/readme-sync.yml \
  assets/flow-line.svg \
  assets/section_quote.svg \
  assets/system-health.svg \
  assets/repo-metrics.svg \
  dist/build-manifest.json \
  health/system_health.json \
  CHANGELOG.md \
  RELEASE_CHECKLIST.md
do
  if [ ! -f "$file" ]; then
    echo "MISSING: $file"
    exit 1
  fi
done
echo "PASS: required files exist"

Expected:

PASS: required files exist

⸻

11. Stage Explicitly

Stage only intended files.

For release documentation updates:

git add \
  CHANGELOG.md \
  RELEASE_CHECKLIST.md

For README surface engine updates:

git add \
  README.base.md \
  README.md \
  Makefile \
  scripts/build_readme.py \
  scripts/quantum_build.sh \
  systems/intelligence/render_status.sh \
  systems/scripts/system_health.sh \
  .github/workflows/readme-sync.yml \
  assets/flow-line.svg \
  assets/section_quote.svg \
  assets/system-health.svg \
  assets/repo-metrics.svg \
  dist/build-manifest.json \
  health/system_health.json

For architecture documentation:

git add docs/*.md

Never stage:

.backups/
docs/STEP_*_OUTPUT.txt
.env
.env.*
*.pem
*.key
credentials.json
service-account.json
node_modules/

⸻

12. Confirm Staged Scope

git diff --cached --name-status
git diff --cached --stat

Check local-only files are not staged:

if git diff --cached --name-only | grep -E '^\.backups/|^docs/STEP_.*_OUTPUT\.txt$|^\.env|\.pem$|\.key$|credentials\.json|service-account\.json'; then
  echo "FAIL: forbidden file staged"
  exit 1
fi
echo "PASS: staged scope clean"

Expected:

PASS: staged scope clean

⸻

13. Final Pre-Commit Gate

make validate
python3 scripts/build_readme.py --dry-run --check
git diff --cached --name-status

Expected:

- validation passes
- dry-run is side-effect free
- staged files match release intent

⸻

14. Commit

Use clear release messages.

Feature release:

git commit -m "feat: release deterministic surface vX.Y.Z"

Pipeline hardening:

git commit -m "chore: harden README surface pipeline"

Bug fix:

git commit -m "fix: repair surface validation gate"

Documentation-only:

git commit -m "docs: add release discipline artifacts"

⸻

15. Push

git push origin main

Expected:

main -> main
local branch aligned with origin/main

⸻

16. Post-Push Verification

git status --short --branch
git log --oneline -5

Inspect:

https://github.com/popdeuxrem/popdeuxrem/actions
https://github.com/popdeuxrem

Expected:

- README Surface Sync workflow is present
- no update-readme workflow exists
- profile README renders correctly
- generated panels render correctly
- latest commit is visible on GitHub

⸻

17. Rollback

If a release breaks README rendering or workflow behavior:

git log --oneline -10
git revert <bad_commit_sha>
make validate
git push origin main

If local files need restoration from backup:

cp -a .backups/pre-release-TIMESTAMP/* .
make validate

If a generated artifact is stale:

make build
make validate
git status --short

⸻

Release Approval

A release is approved only when all are true:

[ ] backup exists for medium/high-risk changes
[ ] make validate passes before mutation
[ ] generator dry-run is side-effect free
[ ] make build passes
[ ] README.md is regenerated from README.base.md
[ ] generated SVG assets exist
[ ] dist/build-manifest.json is valid JSON
[ ] health/system_health.json is valid JSON
[ ] workflow has no git add .
[ ] split-brain workflow is absent
[ ] workflow permissions are explicit
[ ] workflow concurrency exists
[ ] diff is reviewed
[ ] no secrets are staged
[ ] no backup files are staged
[ ] no docs/STEP_*_OUTPUT.txt files are staged
[ ] rollback path is known
[ ] post-push GitHub profile render is verified

