#!/bin/bash

# Configuration
OUTPUT="assets/quantum-terminal.svg"
TITLE="popdeuxrem@system:~/surface"

# Generate tree structure (excluding noisy dirs)
TREE_DATA=$(tree -L 2 -I "__pycache__|dist|node_modules|.git" --noreport)

cat << SVG > $OUTPUT
<svg width="600" height="400" viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="2"/>
  
  <rect width="100%" height="30" rx="10" fill="#161b22"/>
  <circle cx="20" cy="15" r="4" fill="#ff5f56"/>
  <circle cx="35" cy="15" r="4" fill="#ffbd2e"/>
  <circle cx="50" cy="15" r="4" fill="#27c93f"/>
  <text x="300" y="20" font-family="monospace" font-size="12" fill="#8b949e" text-anchor="middle">$TITLE</text>

  <foreignObject x="20" y="50" width="560" height="330">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <style>
        .tree { color: #58a6ff; font-family: 'Courier New', monospace; font-size: 13px; line-height: 1.4; white-space: pre; }
        .dir { color: #d29922; font-weight: bold; }
      </style>
      <div class="tree">$TREE_DATA</div>
    </div>
  </foreignObject>
  
  <rect width="100%" height="100%" fill="url(#scanlines)" opacity="0.05" pointer-events="none"/>
  <defs>
    <pattern id="scanlines" width="100%" height="4" patternUnits="userSpaceOnUse">
      <rect width="100%" height="2" fill="#fff"/>
    </pattern>
  </defs>
</svg>
SVG

echo "◈ Blueprint generated: $OUTPUT"
