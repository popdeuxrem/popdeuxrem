import os
import random
import datetime

def write_svg(filename, content):
    os.makedirs('assets', exist_ok=True)
    with open(f'assets/{filename}', 'w') as f:
        f.write(content)
    print(f"◈ Generated: assets/{filename}")

def gen_hero():
    """ SECTION 1: HERO (Ambient 1000x140) """
    svg = f'''<svg width="1000" height="140" viewBox="0 0 1000 140" xmlns="http://www.w3.org/2000/svg">
    <rect width="1000" height="140" fill="#0d1117"/>
    <defs>
        <mask id="m"><rect width="1000" height="140" fill="white"/></mask>
        <filter id="glow"><feGaussianBlur stdDeviation="1.5" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>
    <style>
        .k-text {{ font-family: sans-serif; font-weight: 900; font-size: 80px; text-transform: uppercase; letter-spacing: -4px; }}
        .ambient-drift {{ animation: drift 45s linear infinite; }}
        @keyframes drift {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
    </style>
    <g mask="url(#m)">
        <text x="0" y="100" class="k-text ambient-drift" fill="#00f3ff" filter="url(#glow)">
            SYSTEMS ARCHITECT ◈ AUTOMATION ◈ PROTOCOLS ◈ SYSTEMS ARCHITECT ◈ AUTOMATION ◈ PROTOCOLS ◈
        </text>
    </g>
    <rect x="0" y="135" width="1000" height="2" fill="#30363d"/>
    <rect x="0" y="135" width="200" height="2" fill="#00f3ff"/>
    </svg>'''
    write_svg('section_hero.svg', svg)

def gen_thesis():
    """ SECTION 2: THESIS (Static 800x250) """
    svg = '''<svg width="800" height="250" viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="250" fill="#050505"/>
    <style>
        .term { font-family: monospace; font-size: 14px; fill: #238636; opacity: 0.9; }
        .keyword { font-weight: bold; fill: #3fb950; }
        .comment { fill: #8b949e; font-style: italic; }
    </style>
    <text x="30" y="40" class="term">> cat /etc/philosophy.conf</text>
    <text x="30" y="80" class="term"><tspan class="keyword">def</tspan> ENGINEERING_THESIS():</text>
    <text x="50" y="110" class="term">    <tspan class="comment"># Complexity is a liability</tspan></text>
    <text x="50" y="130" class="term">    assert <tspan class="keyword">SIMPLICITY</tspan> > ABSTRACTION</text>
    <text x="50" y="160" class="term">    <tspan class="comment"># If you can't measure it, you don't control it</tspan></text>
    <text x="50" y="180" class="term">    require(<tspan class="keyword">OBSERVABILITY</tspan>)</text>
    <text x="50" y="210" class="term">    return <tspan class="keyword">IMMUTABLE_STATE</tspan></text>
    <rect x="0" y="0" width="800" height="250" fill="none" stroke="#30363d" stroke-width="2"/>
    </svg>'''
    write_svg('section_thesis.svg', svg)

def gen_stack():
    """ SECTION 3: STACK (Isometric 800x350) """
    # Mapped to your timeline.json and skills.json data
    cells = [
        ("RUST", 100, 50), ("GO", 300, 50), ("PYTHON", 500, 50),
        ("DOCKER", 100, 150), ("WASM", 300, 150), ("TERRAFORM", 500, 150),
        ("SOLIDITY", 100, 250), ("CI/CD", 300, 250), ("LINUX", 500, 250)
    ]
    rects = ""
    for label, x, y in cells:
        rects += f'''<g transform="translate({x},{y})">
            <path d="M0 20 L80 0 L160 20 L80 40 Z" fill="#161b22" stroke="#bc8cff" stroke-width="1"/>
            <path d="M0 20 V60 L80 80 V40 L0 20 Z" fill="#0d1117" stroke="#bc8cff" stroke-width="1"/>
            <path d="M160 20 V60 L80 80 V40 L160 20 Z" fill="#0d1117" stroke="#bc8cff" stroke-width="1"/>
            <text x="80" y="55" text-anchor="middle" font-family="monospace" font-size="12" fill="#ffffff" font-weight="bold">{label}</text>
        </g>'''
    svg = f'''<svg width="800" height="350" viewBox="0 0 800 350" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="350" fill="#0d1117"/>{rects}</svg>'''
    write_svg('section_stack.svg', svg)

def gen_work():
    """ SECTION 4: WORK (Circuit 600x500) """
    # Mapped to your portfolio.json data
    svg = '''<svg width="600" height="500" viewBox="0 0 600 500" xmlns="http://www.w3.org/2000/svg">
    <rect width="600" height="500" fill="#0d1117"/>
    <defs><filter id="glow"><feGaussianBlur stdDeviation="2.5" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
    <style>
        .trace { stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: flow 3s ease-out forwards; }
        @keyframes flow { to { stroke-dashoffset: 0; } }
        .node-text { font-family: sans-serif; font-size: 14px; font-weight: bold; fill: #d29922; }
    </style>
    <path d="M50 50 V150 H100" stroke="#30363d" stroke-width="2" fill="none"/>
    <path d="M50 150 V300 H100" stroke="#30363d" stroke-width="2" fill="none"/>
    <path d="M50 300 V450 H100" stroke="#30363d" stroke-width="2" fill="none"/>
    <path class="trace" d="M50 50 V150 H100" stroke="#d29922" stroke-width="2" fill="none" filter="url(#glow)"/>
    <path class="trace" d="M50 150 V300 H100" stroke="#d29922" stroke-width="2" fill="none" filter="url(#glow)" style="animation-delay: 0.5s"/>
    <path class="trace" d="M50 300 V450 H100" stroke="#d29922" stroke-width="2" fill="none" filter="url(#glow)" style="animation-delay: 1.0s"/>
    <circle cx="50" cy="50" r="5" fill="#d29922"/>
    
    <rect x="100" y="130" width="400" height="40" rx="4" fill="#161b22" stroke="#d29922"/>
    <text x="120" y="155" class="node-text">SHADOW_SCRIPTS // SECOPS_MESH</text>
    
    <rect x="100" y="280" width="400" height="40" rx="4" fill="#161b22" stroke="#d29922"/>
    <text x="120" y="305" class="node-text">SMOOTH_OPERATOR // AUTO_AGENT</text>
    
    <rect x="100" y="430" width="400" height="40" rx="4" fill="#161b22" stroke="#d29922"/>
    <text x="120" y="455" class="node-text">BRAND_TERMINAL // UI_SURFACE</text>
    </svg>'''
    write_svg('section_work.svg', svg)

def gen_telemetry():
    """ SECTION 5: TELEMETRY (Ambient 800x300) """
    svg = '''<svg width="800" height="300" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="300" fill="#0d1117"/>
    <g transform="translate(400, 150)" opacity="0.6">
        <circle r="100" stroke="#30363d" stroke-width="1" fill="none"/>
        <circle r="70" stroke="#30363d" stroke-width="1" fill="none"/>
        <circle r="40" stroke="#30363d" stroke-width="1" fill="none"/>
        <line x1="-100" y1="0" x2="100" y2="0" stroke="#30363d"/>
        <line x1="0" y1="-100" x2="0" y2="100" stroke="#30363d"/>
        <line x1="0" y1="0" x2="0" y2="-100" stroke="url(#scanGrad)" stroke-width="2">
            <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="8s" repeatCount="indefinite"/>
        </line>
        <circle cx="30" cy="-50" r="3" fill="#ff7b72"><animate attributeName="opacity" values="0.8;0.2;0.8" dur="4s" repeatCount="indefinite"/></circle>
        <circle cx="-40" cy="20" r="2" fill="#ff7b72"><animate attributeName="opacity" values="0.8;0.2;0.8" dur="5.5s" repeatCount="indefinite"/></circle>
    </g>
    <defs><linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#ff7b72"/><stop offset="100%" stop-color="transparent"/></linearGradient></defs>
    <text x="30" y="280" font-family="monospace" font-size="12" fill="#ff7b72" opacity="0.8">LIVE_TELEMETRY // MONITORING</text>
    <text x="650" y="280" font-family="monospace" font-size="12" fill="#ff7b72" opacity="0.8">SIGNAL: NOMINAL</text>
    </svg>'''
    write_svg('section_telemetry.svg', svg)

def gen_security():
    """ SECTION 6: SECURITY (Stripes 1000x40) """
    svg = '''<svg width="1000" height="40" viewBox="0 0 1000 40" xmlns="http://www.w3.org/2000/svg">
    <defs><pattern id="stripes" patternUnits="userSpaceOnUse" width="40" height="40" patternTransform="rotate(45)"><rect width="20" height="40" fill="#d29922"/><rect x="20" width="20" height="40" fill="#0d1117"/></pattern></defs>
    <rect width="1000" height="40" fill="url(#stripes)"/>
    <rect x="300" y="0" width="400" height="40" fill="#0d1117"/>
    <text x="500" y="25" text-anchor="middle" font-family="sans-serif" font-weight="bold" fill="#d29922" letter-spacing="2">SECURITY AUDIT PASSED</text>
    </svg>'''
    write_svg('section_security.svg', svg)
