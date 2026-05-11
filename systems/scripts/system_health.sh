#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HEALTH_DIR="${REPO_ROOT}/health"
LOG_DIR="${REPO_ROOT}/logs"
SYSTEM_HEALTH="${HEALTH_DIR}/system_health.json"
LOG_FILE="${LOG_DIR}/orchestrator.log"

mkdir -p "$HEALTH_DIR" "$LOG_DIR"

json_escape() {
    python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip())[1:-1])'
}

log() {
    local level="$1"
    local msg="$2"
    local timestamp
    timestamp="$(date -Iseconds)"
    printf '[%s] [%s] %s\n' "$timestamp" "$level" "$msg" >> "$LOG_FILE"
}

check_file() {
    local path="$1"
    local name="$2"

    if [[ -f "$path" ]]; then
        local size
        local mod_time
        size="$(stat -c%s "$path" 2>/dev/null || echo "0")"
        mod_time="$(stat -c%y "$path" 2>/dev/null | cut -d'.' -f1 || echo "unknown")"
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
        file_count="$(find "$path" -type f 2>/dev/null | wc -l | tr -d ' ')"
        printf '{"name":"%s","status":"ok","files":%s}' "$name" "$file_count"
    else
        printf '{"name":"%s","status":"missing","files":0}' "$name"
    fi
}

check_scripts() {
    local status="ok"
    local errors=0

    for script in \
        systems/automation/bootstrap.sh \
        systems/automation/healthcheck.sh \
        systems/orchestrator/sync.sh \
        systems/orchestrator/dispatch.sh \
        scripts/build_readme.py \
        scripts/quantum_build.sh
    do
        if [[ -x "$REPO_ROOT/$script" ]]; then
            log "INFO" "Script $script is executable"
        else
            log "ERROR" "Script $script is not executable"
            status="degraded"
            errors=$((errors + 1))
        fi
    done

    printf '{"status":"%s","errors":%d}' "$status" "$errors"
}

check_logs() {
    local log_size=0
    local log_errors=0

    if [[ -f "$LOG_FILE" ]]; then
        log_size="$(stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)"
        log_errors="$(grep -c "ERROR" "$LOG_FILE" 2>/dev/null || true)"
        log_errors="${log_errors:-0}"
    fi

    printf '{"size":%d,"errors":%d}' "$log_size" "$log_errors"
}

derive_overall_status() {
    local payload="$1"

    python3 - "$payload" << 'PY'
import json
import sys

payload = json.loads(sys.argv[1])
components = payload.get("components", {})
statuses = []

for value in components.values():
    if isinstance(value, dict):
        statuses.append(str(value.get("status", "unknown")).lower())

if any(status in {"missing", "fail", "failed", "error", "critical"} for status in statuses):
    print("degraded")
elif any(status in {"degraded", "warn", "warning", "unknown"} for status in statuses):
    print("watch")
else:
    print("healthy")
PY
}

generate_system_health() {
    local automation_health
    automation_health="$(check_file "$HEALTH_DIR/status.json" "automation")"

    local orchestrator_health
    orchestrator_health="$(check_file "$HEALTH_DIR/orchestrator.json" "orchestrator")"

    local metrics_dir
    metrics_dir="$(check_directory "$REPO_ROOT/metrics" "metrics")"

    local identity
    identity="$(check_file "$REPO_ROOT/identity/repos.json" "repos_registry")"

    local scripts_status
    scripts_status="$(check_scripts)"

    local logs_status
    logs_status="$(check_logs)"

    local uptime_value
    uptime_value="$(uptime -p 2>/dev/null || echo "unknown")"

    local git_branch
    local commit_count
    local uncommitted

    git_branch="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")"
    commit_count="$(git -C "$REPO_ROOT" rev-list --count HEAD 2>/dev/null || echo 0)"
    uncommitted="$(git -C "$REPO_ROOT" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"

    local payload
    payload="$(cat <<JSON
{
  "timestamp": "$(date -Iseconds)",
  "uptime": "$uptime_value",
  "components": {
    "automation": $automation_health,
    "orchestrator": $orchestrator_health,
    "metrics": $metrics_dir,
    "identity": $identity,
    "scripts": $scripts_status,
    "logs": $logs_status
  },
  "system": {
    "git_branch": "$git_branch",
    "commit_count": $commit_count,
    "uncommitted_changes": $uncommitted
  }
}
JSON
)"

    local overall
    overall="$(derive_overall_status "$payload")"

    python3 - "$payload" "$overall" > "$SYSTEM_HEALTH" << 'PY'
import json
import sys

payload = json.loads(sys.argv[1])
payload["status"] = sys.argv[2]
print(json.dumps(payload, indent=2, sort_keys=True))
PY

    log "INFO" "System health generated: $SYSTEM_HEALTH"
    cat "$SYSTEM_HEALTH"
}

main() {
    log "INFO" "Generating system health"
    generate_system_health
}

main "$@"
