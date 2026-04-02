#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REGISTRY="${REPO_ROOT}/identity/repos.json"
LOG_FILE="${REPO_ROOT}/logs/orchestrator.log"

log() {
    local level="$1"
    local msg="$2"
    local timestamp
    timestamp=$(date -Iseconds)
    echo "[$timestamp] [$level] $msg" | tee -a "$LOG_FILE"
}

retry() {
    local max_attempts=$1
    local delay=$2
    shift 2
    local cmd=("$@")
    local attempt=1

    while [[ $attempt -le $max_attempts ]]; do
        if "${cmd[@]}" &>/dev/null; then
            return 0
        fi
        log "WARN" "Attempt $attempt/$max_attempts failed"
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

get_repo_by_name() {
    local name="$1"
    local registry_json
    registry_json=$(load_registry)

    if command -v jq &>/dev/null; then
        echo "$registry_json" | jq -r ".repositories[] | select(.name == \"$name\")"
    else
        log "ERROR" "jq required for repo lookup"
        exit 1
    fi
}

dispatch_workflow() {
    local owner="$1"
    local repo="$2"
    local workflow_id="$3"
    local ref="${4:-main}"
    local inputs="${5:-{}}"

    log "INFO" "Dispatching workflow $workflow_id on $owner/$repo (ref: $ref)"

    local api_url="https://api.github.com/repos/$owner/$repo/actions/workflows/$workflow_id/dispatches"

    local response
    if [[ -n "${GITHUB_TOKEN:-}" ]]; then
        response=$(retry 3 5 curl -s -w "\n%{http_code}" \
            -X POST \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            -H "Content-Type: application/json" \
            -d "{\"ref\":\"$ref\",\"inputs\":$inputs}" \
            "$api_url" 2>/dev/null || echo "000")
    else
        log "WARN" "GITHUB_TOKEN not set, using unauthenticated request (rate limited)"
        response=$(retry 1 0 curl -s -w "\n%{http_code}" \
            -X POST \
            -H "Accept: application/vnd.github.v3+json" \
            -H "Content-Type: application/json" \
            -d "{\"ref\":\"$ref\",\"inputs\":$inputs}" \
            "$api_url" 2>/dev/null || echo "000")
    fi

    local http_code
    http_code=$(echo "$response" | tail -n1)

    if [[ "$http_code" == "204" || "$http_code" == "200" ]]; then
        log "INFO" "Workflow triggered successfully on $owner/$repo"
        return 0
    else
        local body
        body=$(echo "$response" | sed '$d')
        log "ERROR" "Failed to dispatch (HTTP $http_code): $body"
        return 1
    fi
}

dispatch_repo() {
    local name="$1"
    local workflow_id="$2"
    local ref="${3:-main}"
    local inputs="${4:-{}}"

    local repo_json
    repo_json=$(get_repo_by_name "$name")

    if [[ -z "$repo_json" || "$repo_json" == "null" ]]; then
        log "ERROR" "Repository not found in registry: $name"
        return 1
    fi

    local owner enabled
    owner=$(echo "$repo_json" | jq -r '.owner')
    enabled=$(echo "$repo_json" | jq -r '.enabled')

    if [[ "$enabled" != "true" ]]; then
        log "WARN" "Repository disabled: $name"
        return 1
    fi

    dispatch_workflow "$owner" "$name" "$workflow_id" "$ref" "$inputs"
}

dispatch_all() {
    local workflow_id="$1"
    local ref="${2:-main}"
    local inputs="${3:-{}}"
    local registry_json
    registry_json=$(load_registry)
    local failed=0

    log "INFO" "Dispatching workflow to all enabled repos"

    local repos
    repos=$(echo "$registry_json" | jq -r '.repositories[] | select(.enabled == true) | @json')

    while IFS= read -r repo_json; do
        [[ -z "$repo_json" ]] && continue

        local name owner type
        name=$(echo "$repo_json" | jq -r '.name')
        owner=$(echo "$repo_json" | jq -r '.owner')
        type=$(echo "$repo_json" | jq -r '.type')

        log "INFO" "Dispatching to $owner/$name (type: $type)"

        if dispatch_workflow "$owner" "$name" "$workflow_id" "$ref" "$inputs"; then
            log "INFO" "Dispatched to $owner/$name"
        else
            log "ERROR" "Failed dispatch to $owner/$name"
            ((failed++))
        fi
    done < <(echo "$repos")

    if [[ $failed -gt 0 ]]; then
        log "WARN" "Dispatch completed with $failed failures"
        return 1
    fi

    log "INFO" "All dispatches completed"
}

update_dashboard() {
    local dashboard_name="${1:-dashboard}"

    log "INFO" "Updating central dashboard: $dashboard_name"

    local repo_json
    repo_json=$(get_repo_by_name "$dashboard_name")

    if [[ -z "$repo_json" || "$repo_json" == "null" ]]; then
        log "ERROR" "Dashboard repo not found: $dashboard_name"
        return 1
    fi

    local owner
    owner=$(echo "$repo_json" | jq -r '.owner')

    local aggregate_file="${REPO_ROOT}/metrics/aggregate.json"
    if [[ -f "$aggregate_file" ]]; then
        log "INFO" "Dashboard metrics available"
    else
        log "WARN" "No aggregate metrics found"
    fi

    dispatch_workflow "$owner" "$dashboard_name" "update.yml" "main" '{"trigger":"orchestrator"}'
}

list_repos() {
    local registry_json
    registry_json=$(load_registry)

    echo "Registered Repositories:"
    echo "$registry_json" | jq -r '.repositories[] | "  \(.name) (\(.type)) - \(.owner) [\(if .enabled then "enabled" else "disabled" end)]"'
}

usage() {
    cat <<EOF
Orchestrator Dispatch - Multi-repo workflow trigger

Usage: $(basename "$0") <command> [options]

Commands:
  dispatch <repo> <workflow> [ref] [inputs]   Dispatch workflow to specific repo
  broadcast <workflow> [ref] [inputs]         Dispatch workflow to all enabled repos
  dashboard [repo]                            Update central dashboard repo
  list                                        List registered repositories

Options:
  GITHUB_TOKEN          Set via env var for authenticated requests

Examples:
  $(basename "$0") dispatch my-repo workflow.yml main '{"key":"value"}'
  $(basename "$0") broadcast build.yml main '{}'
  $(basename "$0") dashboard
  $(basename "$0") list
EOF
}

main() {
    local cmd="${1:-}"
    shift || true

    case "$cmd" in
        dispatch)
            local repo="${1:-}"
            local workflow="${2:-}"
            local ref="${3:-main}"
            local inputs="${4:-{}}"

            if [[ -z "$repo" || -z "$workflow" ]]; then
                log "ERROR" "Missing repo or workflow ID"
                usage
                exit 1
            fi

            dispatch_repo "$repo" "$workflow" "$ref" "$inputs"
            ;;
        broadcast)
            local workflow="${1:-}"
            local ref="${2:-main}"
            local inputs="${3:-{}}"

            if [[ -z "$workflow" ]]; then
                log "ERROR" "Missing workflow ID"
                usage
                exit 1
            fi

            dispatch_all "$workflow" "$ref" "$inputs"
            ;;
        dashboard)
            update_dashboard "${1:-dashboard}"
            ;;
        list)
            list_repos
            ;;
        help|--help|-h)
            usage
            exit 0
            ;;
        *)
            log "ERROR" "Unknown command: $cmd"
            usage
            exit 1
            ;;
    esac
}

main "$@"