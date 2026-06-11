
#!/usr/bin/env bash

set -u

MODE="${1:-build}"

COMMAND_TIMEOUT="${COMMAND_TIMEOUT:-45}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

LOG_FILE="/tmp/popdeuxrem-quantum-check.log"

if [[ "$MODE" != "--check" ]]; then

  LOG_FILE="$ROOT_DIR/dist/build.log"

fi

mkdir -p "$ROOT_DIR/dist"

: > "$LOG_FILE"

ERRORS=0

WARNINGS=0

log() {

  printf '%s\n' "$1"

  printf '%s\n' "$1" >> "$LOG_FILE"

}

pass() {

  log "[PASS] $1"

}

warn() {

  WARNINGS=$((WARNINGS + 1))

  log "[WARN] $1"

}

fail() {

  ERRORS=$((ERRORS + 1))

  log "[FAIL] $1"

}

section() {

  log ""

  log "============================================================"

  log "$1"

}

limited() {

  local seconds="$1"

  shift

  if command -v timeout >/dev/null 2>&1; then

    timeout "$seconds" "$@"

  else

    "$@"

  fi

}

check_python() {

  local file="$1"

  if [[ ! -f "$file" ]]; then

    warn "Missing optional Python file: $file"

    return 0

  fi

  if limited "$COMMAND_TIMEOUT" python3 -m py_compile "$file" >/dev/null 2>/tmp/popdeuxrem-qb.err; then

    pass "Python syntax: $file"

  else

    fail "Python syntax: $file"

    cat /tmp/popdeuxrem-qb.err >> "$LOG_FILE"

  fi

}

check_bash() {

  local file="$1"

  if [[ ! -f "$file" ]]; then

    warn "Missing optional Bash file: $file"

    return 0

  fi

  if limited "$COMMAND_TIMEOUT" bash -n "$file" >/dev/null 2>/tmp/popdeuxrem-qb.err; then

    pass "Bash syntax: $file"

  else

    fail "Bash syntax: $file"

    cat /tmp/popdeuxrem-qb.err >> "$LOG_FILE"

  fi

}

check_json() {

  local file="$1"

  if [[ ! -f "$file" ]]; then

    warn "Missing optional JSON: $file"

    return 0

  fi

  if limited "$COMMAND_TIMEOUT" python3 -m json.tool "$file" >/dev/null 2>/tmp/popdeuxrem-qb.err; then

    pass "Valid JSON: $file"

  else

    fail "Invalid JSON: $file"

    cat /tmp/popdeuxrem-qb.err >> "$LOG_FILE"

  fi

}

check_svg() {

  local file="$1"

  if [[ ! -f "$file" ]]; then

    fail "Missing SVG: $file"

    return 0

  fi

  if grep -q '<svg' "$file"; then

    pass "SVG root: $file"

  else

    fail "Invalid SVG: $file"

  fi

}

check_exists() {

  local file="$1"

  if [[ -f "$file" ]]; then

    pass "Exists: $file"

  else

    fail "Missing: $file"

  fi

}

cd "$ROOT_DIR" || exit 1

log "QUANTUM BUILD LOG - $(date -u +"%Y-%m-%dT%H:%M:%SZ")"

log "MODE: $MODE"

log "ROOT: $ROOT_DIR"

log "COMMAND_TIMEOUT: $COMMAND_TIMEOUT"

section "VALIDATING SCRIPTS"

PYTHON_FILES=(

  "scripts/build_readme.py"

  "scripts/collect_repo_metrics.py"

  "scripts/generate_project_cards.py"

  "scripts/generate_workflow_status.py"

)

BASH_FILES=(

  "scripts/quantum_build.sh"

  "scripts/update_readme.sh"

  "scripts/rollback_surface.sh"

  "systems/intelligence/render_status.sh"

  "systems/scripts/system_health.sh"

)

for file in "${PYTHON_FILES[@]}"; do

  check_python "$file"

done

for file in "${BASH_FILES[@]}"; do

  check_bash "$file"

done

section "VALIDATING JSON"

JSON_FILES=(

  "data/portfolio.json"

  "data/skills.json"

  "data/timeline.json"

  "data/quotes.json"

  "identity/repos.json"

  "health/status.json"

  "health/system_health.json"

  "health/orchestrator.json"

  "metrics/aggregate.json"

  "metrics/metrics.json"

  "assets/projects/index.json"

  "dist/build-manifest.json"

)

for file in "${JSON_FILES[@]}"; do

  check_json "$file"

done

section "VALIDATING README TEMPLATE"

if grep -q '<!-- AUTO-GENERATED:START -->' README.base.md; then

  pass "Template marker: START"

else

  fail "Template marker missing: START"

fi

if grep -q '<!-- AUTO-GENERATED:END -->' README.base.md; then

  pass "Template marker: END"

else

  fail "Template marker missing: END"

fi

section "VALIDATING SVG ASSETS"

SVG_FILES=(

  "assets/flow-line.svg"

  "assets/section_quote.svg"

  "assets/system-health.svg"

  "assets/repo-metrics.svg"

  "assets/workflow-status.svg"

)

for file in "${SVG_FILES[@]}"; do

  check_svg "$file"

done

if [[ -d assets/projects ]]; then

  shopt -s nullglob

  PROJECT_SVGS=(assets/projects/*.svg)

  shopt -u nullglob

  for file in "${PROJECT_SVGS[@]}"; do

    check_svg "$file"

  done

fi

section "GENERATOR CHECK"

if [[ "$MODE" == "--check" ]]; then

  if limited "$COMMAND_TIMEOUT" python3 scripts/build_readme.py --dry-run --check >/tmp/popdeuxrem-generator.out 2>/tmp/popdeuxrem-generator.err; then

    sed 's/^/[GEN] /' /tmp/popdeuxrem-generator.out

    pass "Generator dry-run passed"

  else

    fail "Generator dry-run failed"

    cat /tmp/popdeuxrem-generator.err >> "$LOG_FILE"

  fi

else

  if limited "$COMMAND_TIMEOUT" bash systems/scripts/system_health.sh >/dev/null 2>/tmp/popdeuxrem-health.err; then

    pass "System health generated"

  else

    fail "System health generation failed"

    cat /tmp/popdeuxrem-health.err >> "$LOG_FILE"

  fi

  if limited "$COMMAND_TIMEOUT" python3 scripts/generate_project_cards.py --limit 8 >/dev/null 2>/tmp/popdeuxrem-cards.err; then

    pass "Project cards generated"

  else

    fail "Project cards generation failed"

    cat /tmp/popdeuxrem-cards.err >> "$LOG_FILE"

  fi

  if limited "$COMMAND_TIMEOUT" python3 scripts/generate_workflow_status.py >/dev/null 2>/tmp/popdeuxrem-workflow.err; then

    pass "Workflow status generated"

  else

    fail "Workflow status generation failed"

    cat /tmp/popdeuxrem-workflow.err >> "$LOG_FILE"

  fi

  if limited "$COMMAND_TIMEOUT" python3 scripts/build_readme.py >/tmp/popdeuxrem-generator.out 2>/tmp/popdeuxrem-generator.err; then

    cat /tmp/popdeuxrem-generator.out

    pass "README and assets generated"

  else

    fail "README generation failed"

    cat /tmp/popdeuxrem-generator.err >> "$LOG_FILE"

  fi

fi

section "FINAL VERIFICATION"

REQUIRED_FILES=(

  "README.md"

  "README.base.md"

  "assets/flow-line.svg"

  "assets/section_quote.svg"

  "assets/system-health.svg"

  "assets/repo-metrics.svg"

  "assets/workflow-status.svg"

  "assets/projects/index.json"

  "dist/build-manifest.json"

  "scripts/build_readme.py"

)

for file in "${REQUIRED_FILES[@]}"; do

  check_exists "$file"

done

section "BUILD SUMMARY"

log "Mode: $MODE"

log "Errors: $ERRORS"

log "Warnings: $WARNINGS"

log "Log: $LOG_FILE"

if [[ "$ERRORS" -eq 0 ]]; then

  pass "BUILD COMPLETED SUCCESSFULLY"

  exit 0

fi

fail "BUILD COMPLETED WITH ERRORS"

exit 1

