#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# POPDEUXREM QUANTUM SURFACE v10.0 - UNIFIED BUILD & VERIFICATION SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
ASSETS_DIR="$ROOT_DIR/assets"
DIST_DIR="$ROOT_DIR/dist"
DATA_DIR="$ROOT_DIR/data"
LOG_FILE="$DIST_DIR/build.log"
ERRORS=0
WARNINGS=0

mkdir -p "$DIST_DIR"
echo "QUANTUM BUILD LOG - $(date -u +"%Y-%m-%dT%H:%M:%SZ")" > "$LOG_FILE"

log_info()    { echo "[INFO] $1" | tee -a "$LOG_FILE"; }
log_pass()    { echo "[PASS] $1" | tee -a "$LOG_FILE"; }
log_warn()    { echo "[WARN] $1" | tee -a "$LOG_FILE"; WARNINGS=$((WARNINGS+1)); }
log_fail()    { echo "[FAIL] $1" | tee -a "$LOG_FILE"; ERRORS=$((ERRORS+1)); }
log_section() { echo ""; echo "══════════════════════════════════════════════════════════════" | tee -a "$LOG_FILE"; echo "$1" | tee -a "$LOG_FILE"; }

cd "$ROOT_DIR"

# ═══════════════════════════════════════════════════════════════════════════
# VALIDATE SCRIPTS
# ═══════════════════════════════════════════════════════════════════════════
log_section "◈ VALIDATING SCRIPTS"

for script in build_readme.py discovery.py fetch_telemetry.py update_contrib.sh update_readme.sh vuln_scan.sh; do
    path="$SCRIPT_DIR/$script"
    if [[ -f "$path" ]]; then
        if [[ "$script" == *.py ]]; then
            python3 -m py_compile "$path" 2>/dev/null && log_pass "Python syntax: $script" || log_fail "Python syntax: $script"
        fi
        if [[ "$script" == *.sh ]]; then
            bash -n "$path" 2>/dev/null && log_pass "Bash syntax: $script" || log_fail "Bash syntax: $script"
            chmod +x "$path" 2>/dev/null || true
        fi
    else
        log_warn "Missing: $script"
    fi
done

# ═══════════════════════════════════════════════════════════════════════════
# VALIDATE SVGS
# ═══════════════════════════════════════════════════════════════════════════
log_section "◈ VALIDATING SVG ASSETS"

svg_count=0
for svg in "$ASSETS_DIR"/*.svg; do
    [[ -f "$svg" ]] || continue
    svg_count=$((svg_count+1))
    filename=$(basename "$svg")
    if head -1 "$svg" | grep -q '<svg'; then
        log_pass "Valid header: $filename"
    else
        log_fail "Invalid header: $filename"
    fi
done
log_info "Total SVGs: $svg_count"

# ═══════════════════════════════════════════════════════════════════════════
# VALIDATE DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════
log_section "◈ VALIDATING DEPENDENCIES"

[[ -f "$ROOT_DIR/requirements.txt" ]] && log_pass "Found: requirements.txt" || log_warn "Missing: requirements.txt"

for pkg in requests python-dateutil pyyaml jinja2 pytest; do
    python3 -c "import ${pkg//-/_}" 2>/dev/null && log_pass "Installed: $pkg" || log_warn "Not installed: $pkg"
done

# ═══════════════════════════════════════════════════════════════════════════
# VALIDATE DATA
# ═══════════════════════════════════════════════════════════════════════════
log_section "◈ VALIDATING DATA FILES"

for file in portfolio.json skills.json timeline.json; do
    path="$DATA_DIR/$file"
    if [[ -f "$path" ]]; then
        python3 -c "import json; json.load(open('$path'))" 2>/dev/null && log_pass "Valid JSON: $file" || log_fail "Invalid JSON: $file"
    else
        log_warn "Missing: $file (defaults used)"
    fi
done

# ═══════════════════════════════════════════════════════════════════════════
# GENERATE README
# ═══════════════════════════════════════════════════════════════════════════
log_section "◈ GENERATING README.md"

if python3 "$SCRIPT_DIR/build_readme.py" 2>&1 | tee -a "$LOG_FILE"; then
    log_pass "README.md generated"
else
    log_fail "README.md generation failed"
fi

# ═══════════════════════════════════════════════════════════════════════════
# FINAL CHECK
# ═══════════════════════════════════════════════════════════════════════════
log_section "◈ FINAL VERIFICATION"

for file in README.md assets/hero_banner.svg assets/section_quote.svg scripts/build_readme.py; do
    [[ -f "$ROOT_DIR/$file" ]] && log_pass "Exists: $file" || log_fail "Missing: $file"
done

grep -q "v10.0" "$ROOT_DIR/README.md" 2>/dev/null && log_pass "Version marker: v10.0" || log_warn "Version marker not found"

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
log_section "◈ BUILD SUMMARY"

echo "────────────────────────────────────────────────────────────────" | tee -a "$LOG_FILE"
echo "  Errors:   $ERRORS" | tee -a "$LOG_FILE"
echo "  Warnings: $WARNINGS" | tee -a "$LOG_FILE"
echo "────────────────────────────────────────────────────────────────" | tee -a "$LOG_FILE"

if [[ $ERRORS -eq 0 ]]; then
    log_pass "BUILD COMPLETED SUCCESSFULLY"
    log_info "Log: $LOG_FILE"
    exit 0
else
    log_fail "BUILD COMPLETED WITH ERRORS"
    log_info "Log: $LOG_FILE"
    exit 1
fi