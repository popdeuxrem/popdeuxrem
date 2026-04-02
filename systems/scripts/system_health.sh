#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HEALTH_DIR="${REPO_ROOT}/health"
SYSTEM_HEALTH="${HEALTH_DIR}/system_health.json"
LOG_FILE="${REPO_ROOT}/logs/orchestrator.log"

mkdir -p "$HEALTH_DIR"

log() {
    local level="$1"
    local msg="$2"
    local timestamp
    timestamp=$(date -Iseconds)
    echo "[$timestamp] [$level] $msg" >> "$LOG_FILE"
}

check_file() {
    local path="$1"
    local name="$2"
    
    if [[ -f "$path" ]]; then
        local size
        size=$(stat -c%s "$path" 2>/dev/null || echo "0")
        local mod_time
        mod_time=$(stat -c%y "$path" 2>/dev/null | cut -d'.' -f1 || echo "unknown")
        printf '{"name":"%s","status":"ok","size":%s,"modified":"%s"}' "$name" "$size" "$mod_time"
    else
        printf '{"name":"%s","status":"missing","size":0,"modified":null}' "$name"
    fi
}

check_directory() {
    local path="$1"
    local name="$2"
    
    if [[ -d "$path" ]]; then
        local file_count
        file_count=$(find "$path" -type f 2>/dev/null | wc -l || echo "0")
        printf '{"name":"%s","status":"ok","files":%s}' "$name" "$file_count"
    else
        printf '{"name":"%s","status":"missing","files":0}' "$name"
    fi
}

check_scripts() {
    local status="ok"
    local errors=0
    
    for script in systems/automation/bootstrap.sh systems/automation/healthcheck.sh systems/orchestrator/sync.sh systems/orchestrator/dispatch.sh; do
        if [[ -x "$REPO_ROOT/$script" ]]; then
            log "INFO" "Script $script is executable"
        else
            log "ERROR" "Script $script not executable"
            status="degraded"
            ((errors++))
        fi
    done
    
    printf '{"status":"%s","errors":%d}' "$status" "$errors"
}

check_logs() {
    local log_size=0
    local log_errors=0
    
    if [[ -f "$LOG_FILE" ]]; then
        log_size=$(stat -c%s "$LOG_FILE" 2>/dev/null)
        log_size=${log_size:-0}
        log_errors=$(grep -c "ERROR" "$LOG_FILE" 2>/dev/null) || log_errors=0
    fi
    
    printf '{"size":%d,"errors":%d}' "$log_size" "$log_errors"
}

generate_system_health() {
    local automation_health
    automation_health=$(check_file "$HEALTH_DIR/status.json" "automation")
    
    local orchestrator_health
    orchestrator_health=$(check_file "$HEALTH_DIR/orchestrator.json" "orchestrator")
    
    local metrics_dir
    metrics_dir=$(check_directory "$REPO_ROOT/metrics" "metrics")
    
    local identity
    identity=$(check_file "$REPO_ROOT/identity/repos.json" "repos_registry")
    
    local scripts_status
    scripts_status=$(check_scripts)
    
    local logs_status
    logs_status=$(check_logs)
    
    local uptime
    uptime=$(uptime -p 2>/dev/null || echo "unknown")

    local git_branch commit_count uncommitted
    git_branch=$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    commit_count=$(git -C "$REPO_ROOT" rev-list --count HEAD 2>/dev/null || echo 0)
    uncommitted=$(git -C "$REPO_ROOT" status --porcelain 2>/dev/null | wc -l || echo 0)

    printf '{\n  "timestamp": "%s",\n  "uptime": "%s",\n  "components": {\n    "automation": %s,\n    "orchestrator": %s,\n    "metrics": %s,\n    "identity": %s,\n    "scripts": %s,\n    "logs": %s\n  },\n  "system": {\n    "git_branch": "%s",\n    "commit_count": %d,\n    "uncommitted_changes": %d\n  }\n}\n' \
        "$(date -Iseconds)" \
        "$uptime" \
        "$automation_health" \
        "$orchestrator_health" \
        "$metrics_dir" \
        "$identity" \
        "$scripts_status" \
        "$logs_status" \
        "$git_branch" \
        "$commit_count" \
        "$uncommitted" > "$SYSTEM_HEALTH"

    log "INFO" "System health generated: $SYSTEM_HEALTH"
    cat "$SYSTEM_HEALTH"
}

main() {
    log "INFO" "Generating system health"
    generate_system_health
}

main "$@"