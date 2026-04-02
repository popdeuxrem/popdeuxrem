#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DATE=$(date -Iseconds)

ORCHESTRATOR_HEALTH="{}"
if [[ -f "$REPO_ROOT/health/orchestrator.json" ]]; then
    ORCHESTRATOR_HEALTH=$(cat "$REPO_ROOT/health/orchestrator.json")
fi

SYSTEM_HEALTH="{}"
if [[ -f "$REPO_ROOT/health/system_health.json" ]]; then
    SYSTEM_HEALTH=$(cat "$REPO_ROOT/health/system_health.json")
fi

AGGREGATE_METRICS="{}"
if [[ -f "$REPO_ROOT/metrics/aggregate.json" ]]; then
    AGGREGATE_METRICS=$(cat "$REPO_ROOT/metrics/aggregate.json")
fi

REGISTRY_REPOS="[]"
if [[ -f "$REPO_ROOT/identity/repos.json" ]]; then
    REGISTRY_REPOS=$(cat "$REPO_ROOT/identity/repos.json" | jq -c '.repositories[] | select(.enabled == true) | {name, owner, type}')
fi

REPO_COUNT=0
if command -v jq &>/dev/null && [[ -f "$REPO_ROOT/identity/repos.json" ]]; then
    REPO_COUNT=$(cat "$REPO_ROOT/identity/repos.json" | jq '[.repositories[] | select(.enabled == true)] | length')
fi

cat > README.md <<MD
# ⚙️ Autonomous Repo System

## Status
- Last Update: $DATE

## Commands
\`\`\`bash
make setup
make run
make verify
\`\`\`

## System Health
\`\`\`json
$(echo "$SYSTEM_HEALTH")
\`\`\`

## Local Metrics
\`\`\`json
$(cat "$REPO_ROOT/metrics/metrics.json" 2>/dev/null || echo '{}')
\`\`\`

## Orchestrator Metrics (Aggregate)
\`\`\`json
$AGGREGATE_METRICS
\`\`\`

## Orchestrator Health
\`\`\`json
$ORCHESTRATOR_HEALTH
\`\`\`

## Automation Health
\`\`\`json
$(cat "$REPO_ROOT/health/status.json" 2>/dev/null || echo '{}')
\`\`\`

## Registered Repositories ($REPO_COUNT enabled)
\`\`\`json
$(echo "$REGISTRY_REPOS" | jq -s '.')
\`\`\`

## Architecture
- **systems/automation/** - bootstrap, healthcheck
- **systems/orchestrator/** - sync, dispatch
- **systems/scripts/** - metrics, README, system health
- **metrics/** - local + aggregate metrics
- **health/** - status tracking
- **identity/** - repo registry
- **logs/** - operation logs

## GitHub Actions
- Event-driven: push, pull_request, workflow_dispatch, repository_dispatch
- Scheduled: every 30 minutes

MD