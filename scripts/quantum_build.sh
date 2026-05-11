
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

cd "$ROOT_DIR" || exit 1

log "QUANTUM BUILD LOG - $(date -u +"%Y-%m-%dT%H:%M:%SZ")"

log "MODE: $MODE"

log "ROOT: $ROOT_DIR"

log "COMMAND_TIMEOUT: $COMMAND_TIMEOUT"

section "VALIDATING SCRIPTS"

check_python "scripts/build_readme.py"

check_python "scripts/collect_repo_metrics.py"

check_python "scripts/generate_project_cards.py"

check_python "scripts/generate_workflow_status.py"

check_bash "scripts/quantum_build.sh"

check_bash "scripts/update_readme.sh"

check_bash "scripts/rollback_surface.sh"

check_bash "systems/intelligence/render_status.sh"

check_bash "systems/scripts/system_health.sh"

section "VALIDATING JSON"

check_json "portfolio.json"

check_json "skills.json"

check_json "timeline.json"

check_json "data/quotes.json"

check_json "identity/repos.json"

check_json "health/status.json"

check_json "health/system_health.json"

check_json "health/orchestrator.json"

check_json "metrics/aggregate.json"

check_json "metrics/metrics.json"

check_json "assets/projects/index.json"

check_json "dist/build-manifest.json"

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

check_svg "assets/flow-line.svg"

check_svg "assets/section_quote.svg"

check_svg "assets/system-health.svg"

check_svg "assets/repo-metrics.svg"

check_svg "assets/workflow-status.svg"

if [[ -d assets/projects ]]; then

  for svg in assets/projects/*.svg; do

    [[ -f "$svg" ]] && check_svg "$svg"

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

for file in \

  README.md \

  README.base.md \

  assets/flow-line.svg \

  assets/section_quote.svg \

  assets/system-health.svg \

  assets/repo-metrics.svg \

  assets/workflow-status.svg \

  assets/projects/index.json \

  dist/build-manifest.json \

  scripts/build_readme.py

do

  if [[ -f "$file" ]]; then

    pass "Exists: $file"

  else

    fail "Missing: $file"

  fi

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

