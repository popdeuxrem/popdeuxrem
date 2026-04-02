#!/usr/bin/env bash
set -euo pipefail

COMMITS=$(git rev-list --count HEAD || echo 0)
UPDATED=$(date -Iseconds)

mkdir -p metrics

cat > metrics/metrics.json <<JSON
{
  "commits": $COMMITS,
  "last_updated": "$UPDATED"
}
JSON