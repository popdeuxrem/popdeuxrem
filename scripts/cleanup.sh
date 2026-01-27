#!/bin/bash
# REMOVING LEGACY GENERATORS
rm scripts/generate_axiom.py
rm scripts/generate_capability_matrix.py
rm scripts/generate_glitch_assets.py
rm scripts/generate_glitch_snake.py
rm scripts/generate_header.py
rm scripts/generate_heatline.py
rm scripts/generate_metrics.py
rm scripts/generate_network_graph.py
rm scripts/generate_security_svg.py
rm scripts/generate_skills_radar.py
rm scripts/generate_snake_quote.py
rm scripts/generate_technology_timeline.py
rm scripts/generate_telemetry_panel.py
rm scripts/generate_visuals.py
rm scripts/generate_waveform.py

# REMOVING OLD ASSETS TO FORCE REGENERATION
rm assets/*.svg

echo "◈ Legacy scripts and assets purged."
