#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REGISTRY="${REPO_ROOT}/identity/repos.json"
LOG_FILE="${REPO_ROOT}/logs/orchestrator.log"
METRICS_DIR="${REPO_ROOT}/metrics"
TEMP_DIR="${REPO_ROOT}/tmp/orchestrator"
HEALTH_FILE="${REPO_ROOT}/health/orchestrator.json"

GITHUB_TOKEN="${GITHUB_TOKEN:-}"
AUTH_HEADER=""
if [[ -n "$GITHUB_TOKEN" ]]; then
    AUTH_HEADER="-H Authorization: token $GITHUB_TOKEN"
fi

mkdir -p "$METRICS_DIR" "$TEMP_DIR" "$(dirname "$LOG_FILE")"

log() {
    local level="$1"
    local msg="$2"
    local timestamp
    timestamp=$(date -Iseconds)
    echo "[$timestamp] [$level] $msg" | tee -a "$LOG_FILE"
}

update_health() {
    local status="$1"
    local repos_synced="$2"
    local failures="$3"

    cat > "$HEALTH_FILE" <<EOF
{
  "status": "$status",
  "repos_synced": $repos_synced,
  "failures": $failures,
  "last_sync": "$(date -Iseconds)",
  "github_auth": $(if [[ -n "$GITHUB_TOKEN" ]]; then echo "true"; else echo "false"; fi)
}
EOF
}

validate_metrics() {
    local input_file="$1"
    local errors=0

    if [[ ! -f "$input_file" ]]; then
        log "ERROR" "Validation failed: file not found: $input_file"
        return 1
    fi

    if ! command -v jq &>/dev/null; then
        log "WARN" "jq not available, skipping JSON validation"
        return 0
    fi

    if ! jq -e '.' "$input_file" &>/dev/null; then
        log "ERROR" "Validation failed: invalid JSON in $input_file"
        ((errors++))
    fi

    local repo owner
    repo=$(jq -r '.repo // empty' "$input_file")
    owner=$(jq -r '.owner // empty' "$input_file")

    if [[ -z "$repo" || -z "$owner" ]]; then
        log "ERROR" "Validation failed: missing repo/owner in $input_file"
        ((errors++))
    fi

    if [[ $errors -gt 0 ]]; then
        return 1
    fi

    log "INFO" "Validation passed for $input_file"
    return 0
}

retry() {
    local max_attempts=$1
    local delay=$2
    shift 2
    local cmd=("$@")
    local attempt=1

    while [[ $attempt -le $max_attempts ]]; do
        if "${cmd[@]}"; then
            return 0
        fi
        log "WARN" "Attempt $attempt/${max_attempts} failed for: ${cmd[*]}"
        ((attempt++))
        [[ $attempt -le $max_attempts ]] && sleep "$delay"
    done
    return 1
}

load_registry() {
    if [[ -f "$REGISTRY" ]]; then
        cat "$REGISTRY"
    else
        log "ERROR" "Registry not found: $REGISTRY"
        exit 1
    fi
}

get_repos() {
    local enabled_only="${1:-true}"
    local registry_json
    registry_json=$(load_registry)

    if command -v jq &>/dev/null; then
        if [[ "$enabled_only" == "true" ]]; then
            echo "$registry_json" | jq -r '.repositories[] | select(.enabled == true) | @base64'
        else
            echo "$registry_json" | jq -r '.repositories[] | @base64'
        fi
    else
        log "WARN" "jq not found, using fallback parsing"
        echo "$registry_json" | grep -o '"name": "[^"]*"' | cut -d'"' -f4
    fi
}

parse_repo_field() {
    local repo_json="$1"
    local field="$2"

    if command -v jq &>/dev/null; then
        echo "$repo_json" | jq -r ".$field // empty"
    else
        echo "$repo_json" | grep -o "\"$field\": *\"[^\"]*\"" | cut -d'"' -f4
    fi
}

fetch_repo_metrics() {
    local owner="$1"
    local repo="$2"
    local output_file="$3"

    log "INFO" "Fetching metrics from $owner/$repo"

    local api_url="https://api.github.com/repos/$owner/$repo"
    local response
    response=$(retry 3 5 curl -s -w "\n%{http_code}" $AUTH_HEADER -H "Accept: application/vnd.github.v3+json" "$api_url" 2>/dev/null || echo "000")

    local http_code
    http_code=$(echo "$response" | tail -n1)
    local body
    body=$(echo "$response" | sed '$d')

    if [[ "$http_code" == "200" ]]; then
        local stargazers watchers forks
        stargazers=$(echo "$body" | jq -r '.stargazers_count // 0' 2>/dev/null || echo "0")
        watchers=$(echo "$body" | jq -r '.watchers_count // 0' 2>/dev/null || echo "0")
        forks=$(echo "$body" | jq -r '.forks_count // 0' 2>/dev/null || echo "0")

        cat > "$output_file" <<EOF
{
  "repo": "$repo",
  "owner": "$owner",
  "stargazers": $stargazers,
  "watchers": $watchers,
  "forks": $forks,
  "timestamp": "$(date -Iseconds)"
}
EOF
        log "INFO" "Metrics fetched for $repo: stars=$stargazers"
        return 0
    else
        log "ERROR" "Failed to fetch $repo (HTTP $http_code)"
        return 1
    fi
}

sync_repository() {
    local owner="$1"
    local repo="$2"
    local repo_type="$3"
    local sync_lock="${TEMP_DIR}/${owner}_${repo}.lock"

    if [[ -f "$sync_lock" ]]; then
        local lock_time
        lock_time=$(cat "$sync_lock" 2>/dev/null || echo "0")
        local now
        now=$(date +%s)
        if (( now - lock_time < 3600 )); then
            log "INFO" "Skipping $owner/$repo - recently synced"
            return 0
        fi
    fi

    local metrics_file="${METRICS_DIR}/${owner}_${repo}.json"

    if fetch_repo_metrics "$owner" "$repo" "$metrics_file"; then
        if validate_metrics "$metrics_file"; then
            echo "$(date +%s)" > "$sync_lock"
            log "INFO" "Synced and validated $owner/$repo"
        else
            log "ERROR" "Validation failed for $owner/$repo"
            rm -f "$metrics_file"
            return 1
        fi
    else
        log "ERROR" "Failed to sync $owner/$repo"
        return 1
    fi
}

aggregate_metrics() {
    local output_file="${METRICS_DIR}/aggregate.json"
    local total_stars=0
    local total_watchers=0
    local total_forks=0
    local repo_count=0

    for f in "${METRICS_DIR}"/*.json; do
        [[ -f "$f" ]] || continue
        [[ "$f" == *aggregate* ]] && continue

        if command -v jq &>/dev/null; then
            total_stars=$(( total_stars + $(jq -r '.stargazers // 0' "$f") ))
            total_watchers=$(( total_watchers + $(jq -r '.watchers // 0' "$f") ))
            total_forks=$(( total_forks + $(jq -r '.forks // 0' "$f") ))
            repo_count=$(( repo_count + 1 ))
        fi
    done

    cat > "$output_file" <<EOF
{
  "repos_synced": $repo_count,
  "total_stars": $total_stars,
  "total_watchers": $total_watchers,
  "total_forks": $total_forks,
  "timestamp": "$(date -Iseconds)"
}
EOF
    log "INFO" "Aggregated metrics: $repo_count repos, $total_stars stars"
}

main() {
    log "INFO" "Starting repository sync"
    update_health "running" 0 0

    local failed=0

    while IFS= read -r repo_encoded; do
        [[ -z "$repo_encoded" ]] && continue

        local repo_json
        repo_json=$(echo "$repo_encoded" | base64 -d 2>/dev/null || echo "{}")

        local name owner type enabled
        name=$(parse_repo_field "$repo_json" "name")
        owner=$(parse_repo_field "$repo_json" "owner")
        type=$(parse_repo_field "$repo_json" "type")
        enabled=$(parse_repo_field "$repo_json" "enabled")

        if [[ "$enabled" != "true" ]]; then
            log "INFO" "Skipping disabled repo: $name"
            continue
        fi

        if sync_repository "$owner" "$name" "$type"; then
            log "INFO" "Successfully synced $owner/$name"
        else
            log "ERROR" "Failed to sync $owner/$name"
            ((failed++))
        fi
    done < <(get_repos "true")

    aggregate_metrics

    local synced=0
    for f in "${METRICS_DIR}"/*.json; do
        [[ -f "$f" ]] && [[ "$f" != *aggregate* ]] && synced=$((synced + 1))
    done

    if [[ $failed -gt 0 ]]; then
        update_health "degraded" "$synced" "$failed"
        log "WARN" "Sync completed with $failed failures"
        exit 1
    fi

    update_health "healthy" "$synced" 0
    log "INFO" "Sync completed successfully"
}

main "$@"