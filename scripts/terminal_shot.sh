#!/bin/bash

# terminal-shot.sh v1.0.0
# Purpose: Automate CLI animation capture using centralized config.
# Dependencies: terminalizer (npm install -g terminalizer)

set -e

CONFIG_PATH="config/terminalizer.yml"
OUTPUT_DIR="assets/deployments"
mkdir -p "$OUTPUT_DIR"

if ! command -v terminalizer &> /dev/null; then
    echo "◈ ERROR: terminalizer not found. Install via: npm install -g terminalizer"
    exit 1
fi

record_session() {
    local project_name=$1
    echo "◈ INITIALIZING RECORDING FOR: $project_name"
    echo "◈ Press CTRL+D to stop recording when finished."
    
    terminalizer record "$project_name" --config "$CONFIG_PATH"
}

render_gif() {
    local project_name=$1
    echo "◈ RENDERING GIF..."
    terminalizer render "$project_name" -o "$OUTPUT_DIR/$project_name.gif"
    echo "◈ SUCCESS: $OUTPUT_DIR/$project_name.gif generated."
}

# Main Execution
if [ -z "$1" ]; then
    echo "Usage: bash scripts/terminal_shot.sh <project_name>"
    exit 1
fi

record_session "$1"
render_gif "$1"
