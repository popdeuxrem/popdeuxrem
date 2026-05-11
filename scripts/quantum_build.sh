#!/usr/bin/env bash
# POPDEUXREM QUANTUM SURFACE
# Defensive build and validation gate.

set -u

MODE="${1:-build}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
ASSETS_DIR="$ROOT_DIR/assets"
DIST_DIR="$ROOT_DIR/dist"

ERRORS=0
WARNINGS=0

mkdir -p "$DIST_DIR"

if [[ "$MODE" == "--check" ]]; then
  LOG_FILE="/tmp/popdeuxrem-quantum-check.log"
else
  LOG_FILE="$DIST_DIR/build.log"
fi

: > "$LOG_FILE"

log_line() {
  printf '%s\n' "$1"
  printf '%s\n' "$1" >> "$LOG_FILE"
}

log_section() {
  log_line ""
  log_line "============================================================"
  log_line "$1"
}

log_info() {
  log_line "[INFO] $1"
}

log_pass() {
  log_line "[PASS] $1"
}

log_warn() {
  WARNINGS=$((WARNINGS + 1))
  log_line "[WARN] $1"
}

log_fail() {
  ERRORS=$((ERRORS + 1))
  log_line "[FAIL] $1"
}

run_python_syntax() {
  local file="$1"

  if python3 -m py_compile "$file" >/tmp/popdeuxrem-pycheck.err 2>&1; then
    log_pass "Python syntax: $file"
  else
    log_fail "Python syntax: $file"
    sed 's/^/[PY] /' /tmp/popdeuxrem-pycheck.err >> "$LOG_FILE"
  fi
}

run_bash_syntax() {
  local file="$1"

  if bash -n "$file" >/tmp/popdeuxrem-shcheck.err 2>&1; then
    log_pass "Bash syntax: $file"
  else
    log_fail "Bash syntax: $file"
    sed 's/^/[SH] /' /tmp/popdeuxrem-shcheck.err >> "$LOG_FILE"
  fi
}

validate_json() {
  local file="$1"

  if [[ ! -f "$file" ]]; then
    log_warn "Missing optional JSON: $file"
    return 0
  fi

  if python3 -m json.tool "$file" >/tmp/popdeuxrem-jsoncheck.out 2>/tmp/popdeuxrem-jsoncheck.err; then
    log_pass "Valid JSON: $file"
  else
    log_fail "Invalid JSON: $file"
    sed 's/^/[JSON] /' /tmp/popdeuxrem-jsoncheck.err >> "$LOG_FILE"
  fi
}

validate_import() {
  local package="$1"
  local import_name="$2"

  if python3 -c "import ${import_name}" >/dev/null 2>&1; then
    log_pass "Installed: $package"
  else
    log_warn "Not installed: $package"
  fi
}

cd "$ROOT_DIR" || {
  log_fail "Unable to cd into repo root: $ROOT_DIR"
  exit 1
}

log_line "QUANTUM BUILD LOG - $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
log_line "MODE: $MODE"
log_line "ROOT: $ROOT_DIR"

log_section "VALIDATING SCRIPTS"

for script in \
  scripts/build_readme.py \
  scripts/update_readme.sh \
  scripts/quantum_build.sh \
  systems/automation/bootstrap.sh \
  systems/automation/healthcheck.sh \
  systems/intelligence/render_status.sh \
  systems/orchestrator/dispatch.sh \
  systems/orchestrator/sync.sh \
  systems/scripts/generate_metrics.sh \
  systems/scripts/generate_readme.sh \
  systems/scripts/system_health.sh
do
  if [[ ! -f "$script" ]]; then
    log_warn "Missing optional script: $script"
    continue
  fi

  case "$script" in
    *.py)
      run_python_syntax "$script"
      ;;
    *.sh)
      run_bash_syntax "$script"
      ;;
    *)
      log_warn "Unknown script type: $script"
      ;;
  esac
done

log_section "VALIDATING JSON DATA"

for file in \
  portfolio.json \
  skills.json \
  timeline.json \
  data/quotes.json \
  identity/repos.json \
  health/status.json \
  health/system_health.json \
  health/orchestrator.json \
  metrics/aggregate.json \
  metrics/metrics.json \
  metrics/popdeuxrem_popdeuxrem.json
do
  validate_json "$file"
done

log_section "VALIDATING DEPENDENCIES"

if [[ -f requirements.txt ]]; then
  log_pass "Found: requirements.txt"
else
  log_warn "Missing: requirements.txt"
fi

validate_import "requests" "requests"
validate_import "python-dateutil" "dateutil"
validate_import "pyyaml" "yaml"
validate_import "jinja2" "jinja2"
validate_import "pytest" "pytest"

log_section "VALIDATING README TEMPLATE"

if [[ -f README.base.md ]]; then
  if grep -q '<!-- AUTO-GENERATED:START -->' README.base.md; then
    log_pass "Template marker: START"
  else
    log_fail "Template marker missing: START"
  fi

  if grep -q '<!-- AUTO-GENERATED:END -->' README.base.md; then
    log_pass "Template marker: END"
  else
    log_fail "Template marker missing: END"
  fi
else
  log_fail "Missing: README.base.md"
fi

log_section "VALIDATING SVG ASSETS"

svg_count=0

if compgen -G "$ASSETS_DIR/*.svg" >/dev/null; then
  for svg in "$ASSETS_DIR"/*.svg; do
    svg_count=$((svg_count + 1))
    filename="$(basename "$svg")"

    if grep -q '<svg' "$svg"; then
      log_pass "SVG contains root: $filename"
    else
      log_fail "Invalid SVG: $filename"
    fi
  done
else
  log_warn "No SVG assets found"
fi

log_info "Total SVGs: $svg_count"

log_section "GENERATOR CHECK"

if [[ "$MODE" == "--check" ]]; then
  if python3 scripts/build_readme.py --dry-run --check >/tmp/popdeuxrem-generator.out 2>/tmp/popdeuxrem-generator.err; then
    sed 's/^/[GEN] /' /tmp/popdeuxrem-generator.out
    cat /tmp/popdeuxrem-generator.out >> "$LOG_FILE"
    log_pass "Generator dry-run passed"
  else
    log_fail "Generator dry-run failed"
    sed 's/^/[GEN-ERR] /' /tmp/popdeuxrem-generator.err
    sed 's/^/[GEN-ERR] /' /tmp/popdeuxrem-generator.err >> "$LOG_FILE"
  fi
else
  if bash systems/scripts/system_health.sh >/tmp/popdeuxrem-health.out 2>/tmp/popdeuxrem-health.err; then
    log_pass "System health generated"
  else
    log_fail "System health generation failed"
    sed 's/^/[HEALTH-ERR] /' /tmp/popdeuxrem-health.err >> "$LOG_FILE"
  fi

  if python3 scripts/build_readme.py >/tmp/popdeuxrem-generator.out 2>/tmp/popdeuxrem-generator.err; then
    cat /tmp/popdeuxrem-generator.out
    cat /tmp/popdeuxrem-generator.out >> "$LOG_FILE"
    log_pass "README and assets generated"
  else
    log_fail "README generation failed"
    sed 's/^/[GEN-ERR] /' /tmp/popdeuxrem-generator.err
    sed 's/^/[GEN-ERR] /' /tmp/popdeuxrem-generator.err >> "$LOG_FILE"
  fi
fi

log_section "FINAL VERIFICATION"

for file in \
  README.md \
  README.base.md \
  assets/flow-line.svg \
  assets/section_quote.svg \
  scripts/build_readme.py
do
  if [[ -f "$file" ]]; then
    log_pass "Exists: $file"
  else
    log_fail "Missing: $file"
  fi
done

if [[ "$MODE" == "build" ]]; then
  for file in \
    assets/system-health.svg \
    assets/repo-metrics.svg \
    dist/build-manifest.json
  do
    if [[ -f "$file" ]]; then
      log_pass "Exists: $file"
    else
      log_fail "Missing: $file"
    fi
  done
fi

log_section "BUILD SUMMARY"

log_line "Mode: $MODE"
log_line "Errors: $ERRORS"
log_line "Warnings: $WARNINGS"
log_line "Log: $LOG_FILE"

if [[ "$ERRORS" -eq 0 ]]; then
  log_pass "BUILD COMPLETED SUCCESSFULLY"
  exit 0
fi

log_fail "BUILD COMPLETED WITH ERRORS"
exit 1
