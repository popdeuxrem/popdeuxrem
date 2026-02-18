import os
import random
import datetime
import json

def write_svg(filename, content):
    os.makedirs('assets', exist_ok=True)
    with open(f'assets/{filename}', 'w') as f:
        f.write(content)
    print(f"◈ Generated: assets/{filename}")

def gen_hero():
    """ SECTION 1: HERO (Ambient 1000x140) """
    svg = '''<svg width="1000" height="140" viewBox="0 0 1000 140" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="quantum-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00f3ff;stop-opacity:0.8"/>
      <stop offset="50%" style="stop-color:#bc8cff;stop-opacity:0.6"/>
      <stop offset="100%" style="stop-color:#00f3ff;stop-opacity:0.8"/>
    </linearGradient>
    
    <linearGradient id="boot-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="100%" style="stop-color:#161b22"/>
    </linearGradient>
    
    <filter id="glow-cyan" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feFlood flood-color="#00f3ff" flood-opacity="0.5"/>
      <feComposite in2="blur" operator="in"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <filter id="glow-magenta" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feFlood flood-color="#bc8cff" flood-opacity="0.4"/>
      <feComposite in2="blur" operator="in"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <filter id="particle-glow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="1" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <style>
    .bg-fill { fill: #0d1117; }
    .bg-fill-light { fill: #f6f8fa; }
    .text-primary { fill: #00f3ff; }
    .text-primary-light { fill: #0969da; }
    .text-accent { fill: #bc8cff; }
    .text-accent-light { fill: #8250df; }
    .text-muted { fill: #484f58; }
    .text-muted-light { fill: #57606a; }
    .particle { fill: #00f3ff; opacity: 0.6; }
    .particle-light { fill: #0969da; opacity: 0.5; }
    .border-line { stroke: #30363d; }
    .border-line-light { stroke: #d0d7de; }
    
    .username { 
      font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
      font-weight: 800; 
      font-size: 28px; 
      letter-spacing: -0.5px;
    }
    
    .role-text { 
      font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; 
      font-size: 11px; 
      letter-spacing: 1.5px;
      text-transform: uppercase;
    }
    
    .tagline-text { 
      font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; 
      font-size: 10px; 
      letter-spacing: 0.5px;
    }
    
    .ascii-decor {
      font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
      font-size: 8px;
      fill: #30363d;
    }
    
    .ascii-decor-light {
      font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
      font-size: 8px;
      fill: #8c959f;
    }
    
    .cursor { animation: blink 1s step-end infinite; }
    @keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0; } }
    
    .particle-1 { animation: float-p1 8s ease-in-out infinite; }
    .particle-2 { animation: float-p2 12s ease-in-out infinite; }
    .particle-3 { animation: float-p3 10s ease-in-out infinite; }
    .particle-4 { animation: float-p4 15s ease-in-out infinite; }
    .particle-5 { animation: float-p5 7s ease-in-out infinite; }
    .particle-6 { animation: float-p6 11s ease-in-out infinite; }
    .particle-7 { animation: float-p7 9s ease-in-out infinite; }
    .particle-8 { animation: float-p8 14s ease-in-out infinite; }
    
    @keyframes float-p1 { 0%, 100% { transform: translate(0, 0); } 25% { transform: translate(20px, -15px); } 50% { transform: translate(40px, 5px); } 75% { transform: translate(15px, 10px); } }
    @keyframes float-p2 { 0%, 100% { transform: translate(0, 0); } 33% { transform: translate(-25px, 20px); } 66% { transform: translate(10px, -10px); } }
    @keyframes float-p3 { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(-30px, -20px); } }
    @keyframes float-p4 { 0%, 100% { transform: translate(0, 0); } 25% { transform: translate(15px, 25px); } 75% { transform: translate(-20px, -15px); } }
    @keyframes float-p5 { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(25px, 15px); } }
    @keyframes float-p6 { 0%, 100% { transform: translate(0, 0); } 33% { transform: translate(-15px, -25px); } 66% { transform: translate(20px, 10px); } }
    @keyframes float-p7 { 0%, 100% { transform: translate(0, 0); } 25% { transform: translate(30px, 10px); } 75% { transform: translate(-10px, -20px); } }
    @keyframes float-p8 { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(-20px, 20px); } }
    
    .boot-line { opacity: 0; }
    .boot-1 { animation: boot-appear 0.5s ease-out 0.2s forwards; }
    .boot-2 { animation: boot-appear 0.5s ease-out 0.5s forwards; }
    .boot-3 { animation: boot-appear 0.5s ease-out 0.8s forwards; }
    .boot-4 { animation: boot-appear 0.5s ease-out 1.1s forwards; }
    .boot-5 { animation: boot-appear 0.5s ease-out 1.4s forwards; }
    .boot-6 { animation: boot-appear 0.5s ease-out 1.7s forwards; }
    
    @keyframes boot-appear { 0% { opacity: 0; transform: translateX(-10px); } 100% { opacity: 1; transform: translateX(0); } }
    
    .username-reveal { 
      opacity: 0;
      animation: username-type 2s ease-out 2s forwards; 
    }
    @keyframes username-type { 0% { opacity: 0; } 100% { opacity: 1; } }
    
    .scan-line {
      animation: scan 4s linear infinite;
    }
    @keyframes scan { 0% { transform: translateY(-140px); } 100% { transform: translateY(140px); } }
    
    @media (prefers-color-scheme: light) {
      .bg-fill { fill: #f6f8fa; }
      .text-primary { fill: #0969da; }
      .text-accent { fill: #8250df; }
      .text-muted { fill: #57606a; }
      .particle { fill: #0969da; opacity: 0.4; }
      .ascii-decor { fill: #8c959f; }
      .border-line { stroke: #d0d7de; }
    }
    
    @media (prefers-reduced-motion: reduce) {
      .particle-1, .particle-2, .particle-3, .particle-4,
      .particle-5, .particle-6, .particle-7, .particle-8,
      .cursor, .scan-line {
        animation: none;
      }
      .boot-line, .username-reveal {
        animation: none;
        opacity: 1;
      }
    }
  </style>
  
  <!-- Background -->
  <rect class="bg-fill" width="1000" height="140"/>
  
  <!-- Particle Field Background -->
  <g filter="url(#particle-glow)">
    <circle class="particle particle-1" cx="50" cy="30" r="2"/>
    <circle class="particle particle-2" cx="150" cy="110" r="1.5"/>
    <circle class="particle particle-3" cx="280" cy="45" r="2.5"/>
    <circle class="particle particle-4" cx="400" cy="95" r="1"/>
    <circle class="particle particle-5" cx="550" cy="25" r="2"/>
    <circle class="particle particle-6" cx="700" cy="115" r="1.5"/>
    <circle class="particle particle-7" cx="850" cy="40" r="2"/>
    <circle class="particle particle-8" cx="950" cy="100" r="1"/>
    <circle class="particle particle-1" cx="120" cy="70" r="1"/>
    <circle class="particle particle-3" cx="350" cy="120" r="1.5"/>
    <circle class="particle particle-5" cx="620" cy="55" r="1"/>
    <circle class="particle particle-7" cx="780" cy="85" r="1.5"/>
  </g>
  
  <!-- Subtle grid pattern -->
  <g opacity="0.05">
    <line x1="0" y1="35" x2="1000" y2="35" stroke="#00f3ff" stroke-width="0.5"/>
    <line x1="0" y1="70" x2="1000" y2="70" stroke="#00f3ff" stroke-width="0.5"/>
    <line x1="0" y1="105" x2="1000" y2="105" stroke="#00f3ff" stroke-width="0.5"/>
  </g>
  
  <!-- ASCII Decorative Elements -->
  <text class="ascii-decor" x="15" y="20">╔══════════════════════════════════════╗</text>
  <text class="ascii-decor" x="15" y="130">╚══════════════════════════════════════╝</text>
  <text class="ascii-decor" x="900" y="20">┌─────────────────┐</text>
  <text class="ascii-decor" x="900" y="130">└─────────────────┘</text>
  
  <!-- Terminal Boot Sequence -->
  <g font-family="'SF Mono', 'Fira Code', 'Consolas', monospace" font-size="9">
    <text class="text-muted boot-line boot-1" x="30" y="38">[ BOOT ] Initializing quantum subsystems...</text>
    <text class="text-primary boot-line boot-2" x="30" y="52">[ OK ] Protocol stack loaded</text>
    <text class="text-accent boot-line boot-3" x="30" y="66">[ OK ] Neural interfaces calibrated</text>
    <text class="text-muted boot-line boot-4" x="30" y="80">[ INFO ] Establishing secure channels...</text>
    <text class="text-primary boot-line boot-5" x="30" y="94">[ READY ] System operational</text>
  </g>
  
  <!-- Main Username Display -->
  <g class="username-reveal">
    <text class="username text-primary" x="420" y="62" filter="url(#glow-cyan)">PopDeuxRem</text>
    <rect class="cursor" x="598" y="45" width="2" height="22" fill="#00f3ff"/>
  </g>
  
  <!-- Role Badge -->
  <g transform="translate(420, 78)">
    <rect x="0" y="-10" width="220" height="14" rx="2" fill="#00f3ff" fill-opacity="0.1" stroke="#00f3ff" stroke-width="0.5" stroke-opacity="0.3"/>
    <text class="role-text text-primary" x="8" y="1">PRINCIPAL SYSTEMS ARCHITECT</text>
  </g>
  
  <!-- Tagline -->
  <text class="tagline-text text-accent" x="420" y="102" filter="url(#glow-magenta)">"Building quantum-grade infrastructure"</text>
  
  <!-- Decorative Status Indicators -->
  <g transform="translate(870, 50)">
    <circle cx="0" cy="0" r="4" fill="#00f3ff" opacity="0.8">
      <animate attributeName="opacity" values="0.8;0.3;0.8" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text class="ascii-decor" x="10" y="3">STATUS: ONLINE</text>
    
    <circle cx="0" cy="20" r="4" fill="#bc8cff" opacity="0.8">
      <animate attributeName="opacity" values="0.8;0.3;0.8" dur="1.5s" repeatCount="indefinite"/>
    </circle>
    <text class="ascii-decor" x="10" y="23">SYNC: ACTIVE</text>
    
    <circle cx="0" cy="40" r="4" fill="#3fb950" opacity="0.8">
      <animate attributeName="opacity" values="0.8;0.3;0.8" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <text class="ascii-decor" x="10" y="43">MODE: QUANTUM</text>
  </g>
  
  <!-- Bottom Accent Line -->
  <line class="border-line" x1="0" y1="138" x2="1000" y2="138" stroke-width="2"/>
  <rect x="0" y="137" width="300" height="3" fill="url(#quantum-gradient)">
    <animate attributeName="width" values="0;1000;0" dur="8s" repeatCount="indefinite"/>
  </rect>
  
  <!-- Version indicator -->
  <text class="ascii-decor" x="30" y="118">v2.0.47 // build:2024.stable</text>
</svg>'''
    write_svg('section_hero.svg', svg)

def gen_thesis():
    """ SECTION 2: THESIS (Static 800x250) """
    svg = '''<svg width="800" height="250" viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            @keyframes pulse-quantum {
                0%, 100% { opacity: 0.6; }
                50% { opacity: 1; }
            }
            @keyframes fade-in {
                from { opacity: 0; transform: translateY(8px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes wave-drift {
                from { transform: translateX(0); }
                to { transform: translateX(-40px); }
            }
            .quantum-pulse { animation: pulse-quantum 2.5s ease-in-out infinite; }
            .fade-1 { animation: fade-in 0.8s ease-out forwards; animation-delay: 0.1s; opacity: 0; }
            .fade-2 { animation: fade-in 0.8s ease-out forwards; animation-delay: 0.3s; opacity: 0; }
            .fade-3 { animation: fade-in 0.8s ease-out forwards; animation-delay: 0.5s; opacity: 0; }
            .wave-animate { animation: wave-drift 8s linear infinite; }
            @media (prefers-reduced-motion) {
                .quantum-pulse, .wave-animate { animation: none; opacity: 0.8; }
                .fade-1, .fade-2, .fade-3 { animation: none; opacity: 1; }
            }
        </style>
        <linearGradient id="panel-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0d1117"/>
            <stop offset="100%" stop-color="#161b22"/>
        </linearGradient>
        <linearGradient id="quantum-glow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#3fb950" stop-opacity="0"/>
            <stop offset="50%" stop-color="#3fb950" stop-opacity="1"/>
            <stop offset="100%" stop-color="#3fb950" stop-opacity="0"/>
        </linearGradient>
        <filter id="glow-soft">
            <feGaussianBlur stdDeviation="2" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
    </defs>

    <rect width="800" height="250" fill="url(#panel-gradient)"/>

    <g class="wave-animate">
        <text x="0" y="45" font-family="monospace" font-size="11" fill="#3fb950" opacity="0.15">
            ~~⟨ψ|φ⟩~~  ∿∿∿  ~~⟨ψ|φ⟩~~  ∿∿∿  ~~⟨ψ|φ⟩~~  ∿∿∿  ~~⟨ψ|φ⟩~~  ∿∿∿  ~~⟨ψ|φ⟩~~  ∿∿∿  ~~⟨ψ|φ⟩~~  ∿∿∿  ~~⟨ψ|φ⟩~~
        </text>
    </g>

    <line x1="280" y1="60" x2="280" y2="190" stroke="#30363d" stroke-width="1"/>

    <g class="quantum-pulse">
        <circle cx="280" cy="60" r="4" fill="#3fb950" filter="url(#glow-soft)"/>
        <circle cx="280" cy="125" r="6" fill="#3fb950" filter="url(#glow-soft)"/>
        <circle cx="280" cy="190" r="4" fill="#3fb950" filter="url(#glow-soft)"/>
    </g>

    <g class="fade-1">
        <text x="45" y="95" font-family="Georgia, serif" font-size="13" fill="#8b949e" font-style="italic">
            THESIS
        </text>
        <text x="45" y="120" font-family="monospace" font-size="11" fill="#3fb950" letter-spacing="2">
            ⟨ QUANTUM OBSERVABILITY ⟩
        </text>
    </g>

    <g class="fade-2">
        <text x="45" y="155" font-family="monospace" font-size="10" fill="#8b949e" opacity="0.7">
            state: SUPERPOSITION
        </text>
        <text x="45" y="172" font-family="monospace" font-size="10" fill="#8b949e" opacity="0.7">
            probability: |ψ|² = 1.0
        </text>
    </g>

    <g class="fade-3">
        <rect x="310" y="70" width="450" height="115" rx="2" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
        <line x1="310" y1="70" x2="760" y2="70" stroke="#3fb950" stroke-width="2"/>
        
        <text x="335" y="105" font-family="Georgia, serif" font-size="15" fill="#e6edf3">
            <tspan>I architect systems that </tspan><tspan fill="#3fb950">fail gracefully</tspan><tspan>,</tspan>
        </text>
        <text x="335" y="128" font-family="Georgia, serif" font-size="15" fill="#e6edf3">
            <tspan>scale infinitely, and tell you when</tspan>
        </text>
        <text x="335" y="151" font-family="Georgia, serif" font-size="15" fill="#e6edf3">
            <tspan>they're </tspan><tspan fill="#8b949e" font-style="italic">unhappy</tspan><tspan>.</tspan>
        </text>
        
        <line x1="335" y1="165" x2="735" y2="165" stroke="#21262d" stroke-width="1" stroke-dasharray="4,4"/>
        
        <text x="335" y="182" font-family="monospace" font-size="10" fill="#8b949e">
            &gt; complexity = debt; observability = currency
        </text>
    </g>

    <g class="quantum-pulse">
        <rect x="310" y="200" width="120" height="3" fill="url(#quantum-glow)" rx="1"/>
        <rect x="445" y="200" width="80" height="3" fill="url(#quantum-glow)" rx="1"/>
        <rect x="540" y="200" width="100" height="3" fill="url(#quantum-glow)" rx="1"/>
        <rect x="655" y="200" width="60" height="3" fill="url(#quantum-glow)" rx="1"/>
    </g>

    <g class="wave-animate">
        <text x="0" y="235" font-family="monospace" font-size="11" fill="#3fb950" opacity="0.15">
            ∿∿∿  ~~⟨ψ|φ⟩~~  ∿∿∿  ~~⟨ψ|φ⟩~~  ∿∿∿  ~~⟨ψ|φ⟩~~  ∿∿∿  ~~⟨ψ|φ⟩~~  ∿∿∿  ~~⟨ψ|φ⟩~~  ∿∿∿  ~~⟨ψ|φ⟩~~
        </text>
    </g>

    <style>
        @media (prefers-color-scheme: light) {
            rect { fill: #f6f8fa !important; }
            line[stroke="#30363d"] { stroke: #d0d7de !important; }
            text[fill="#e6edf3"] { fill: #1f2328 !important; }
            text[fill="#8b949e"] { fill: #656d76 !important; }
            rect[fill="#0d1117"] { fill: #ffffff !important; }
        }
    </style>
</svg>
'''
    write_svg('section_thesis.svg', svg)

def gen_stack():
    """ SECTION 3: STACK (Isometric 800x350) """
    svg = '''<svg width="800" height="350" viewBox="0 0 800 350" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg { fill: var(--bg-color, #0d1117); }
    .text-primary { fill: var(--text-color, #e6edf3); }
    .text-muted { fill: var(--muted-color, #7d8590); }
    .bar-bg { fill: var(--bar-bg, #21262d); }
    .terminal-header { fill: var(--header-bg, #161b22); }
    @media (prefers-color-scheme: light) {
      .bg { fill: #f6f8fa; }
      .text-primary { fill: #1f2328; }
      .text-muted { fill: #656d76; }
      .bar-bg { fill: #d1d9e0; }
      .terminal-header { fill: #e6e9ec; }
    }
  </style>
  
  <rect class="bg" width="800" height="350" rx="8"/>
  
  <rect class="terminal-header" x="20" y="20" width="760" height="36" rx="6"/>
  <circle cx="40" cy="38" r="6" fill="#ff5f56"/>
  <circle cx="60" cy="38" r="6" fill="#ffbd2e"/>
  <circle cx="80" cy="38" r="6" fill="#27ca40"/>
  <text x="400" y="44" text-anchor="middle" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="14" class="text-muted">~/skills --analyze</text>
  
  <g transform="translate(40, 80)">
    <g transform="translate(0, 0)">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <rect width="24" height="24" rx="3" fill="#3178c6"/>
        <text x="12" y="17" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#fff">TS</text>
      </svg>
      <text x="36" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="15" class="text-primary">TypeScript</text>
      <text x="140" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">[</text>
      <rect class="bar-bg" x="150" y="5" width="500" height="14" rx="2"/>
      <rect x="150" y="5" width="0" height="14" rx="2" fill="url(#grad95)">
        <animate attributeName="width" from="0" to="475" dur="1.2s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>
      </rect>
      <text x="658" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">]</text>
      <text x="720" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="14" fill="#00f3ff">95%</text>
    </g>
    
    <g transform="translate(0, 38)">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <rect width="24" height="24" rx="3" fill="#7b42bc"/>
        <path d="M7 7h10v2H7zM7 11h10v2H7zM7 15h7v2H7z" fill="#fff"/>
      </svg>
      <text x="36" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="15" class="text-primary">Terraform</text>
      <text x="140" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">[</text>
      <rect class="bar-bg" x="150" y="5" width="500" height="14" rx="2"/>
      <rect x="150" y="5" width="0" height="14" rx="2" fill="url(#grad90)">
        <animate attributeName="width" from="0" to="450" dur="1.3s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>
      </rect>
      <text x="658" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">]</text>
      <text x="720" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="14" fill="#00e5ff">90%</text>
    </g>
    
    <g transform="translate(0, 76)">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <rect width="24" height="24" rx="3" fill="#3776ab"/>
        <circle cx="12" cy="12" r="5" fill="#ffd43b"/>
        <circle cx="12" cy="12" r="2.5" fill="#3776ab"/>
      </svg>
      <text x="36" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="15" class="text-primary">Python</text>
      <text x="140" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">[</text>
      <rect class="bar-bg" x="150" y="5" width="500" height="14" rx="2"/>
      <rect x="150" y="5" width="0" height="14" rx="2" fill="url(#grad85)">
        <animate attributeName="width" from="0" to="425" dur="1.4s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>
      </rect>
      <text x="658" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">]</text>
      <text x="720" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="14" fill="#00d7ff">85%</text>
    </g>
    
    <g transform="translate(0, 114)">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <rect width="24" height="24" rx="3" fill="#00add8"/>
        <text x="12" y="17" text-anchor="middle" font-family="monospace" font-size="14" font-weight="bold" fill="#fff">Go</text>
      </svg>
      <text x="36" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="15" class="text-primary">Go</text>
      <text x="140" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">[</text>
      <rect class="bar-bg" x="150" y="5" width="500" height="14" rx="2"/>
      <rect x="150" y="5" width="0" height="14" rx="2" fill="url(#grad80)">
        <animate attributeName="width" from="0" to="400" dur="1.5s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>
      </rect>
      <text x="658" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">]</text>
      <text x="720" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="14" fill="#00c8ff">80%</text>
    </g>
    
    <g transform="translate(0, 152)">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <rect width="24" height="24" rx="3" fill="#dea584"/>
        <circle cx="12" cy="12" r="6" fill="none" stroke="#705e4d" stroke-width="2"/>
        <circle cx="12" cy="12" r="3" fill="#705e4d"/>
      </svg>
      <text x="36" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="15" class="text-primary">Rust</text>
      <text x="140" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">[</text>
      <rect class="bar-bg" x="150" y="5" width="500" height="14" rx="2"/>
      <rect x="150" y="5" width="0" height="14" rx="2" fill="url(#grad70)">
        <animate attributeName="width" from="0" to="350" dur="1.6s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>
      </rect>
      <text x="658" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">]</text>
      <text x="720" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="14" fill="#5ce1ff">70%</text>
    </g>
    
    <g transform="translate(0, 190)">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <rect width="24" height="24" rx="3" fill="#363636"/>
        <polygon points="12,4 20,8 20,12 12,16 4,12 4,8" fill="#6c6c6c" stroke="#fff" stroke-width="0.5"/>
        <polygon points="12,8 16,10 16,14 12,16 8,14 8,10" fill="#999"/>
      </svg>
      <text x="36" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="15" class="text-primary">Solidity</text>
      <text x="140" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">[</text>
      <rect class="bar-bg" x="150" y="5" width="500" height="14" rx="2"/>
      <rect x="150" y="5" width="0" height="14" rx="2" fill="url(#grad60)">
        <animate attributeName="width" from="0" to="300" dur="1.7s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>
      </rect>
      <text x="658" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="13" class="text-muted">]</text>
      <text x="720" y="17" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="14" fill="#bc8cff">60%</text>
    </g>
  </g>
  
  <defs>
    <linearGradient id="grad95" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f3ff"/>
      <stop offset="100%" stop-color="#00f3ff"/>
    </linearGradient>
    <linearGradient id="grad90" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f3ff"/>
      <stop offset="33%" stop-color="#3de0ff"/>
      <stop offset="100%" stop-color="#7accff"/>
    </linearGradient>
    <linearGradient id="grad85" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f3ff"/>
      <stop offset="50%" stop-color="#5cd0ff"/>
      <stop offset="100%" stop-color="#9fb8ff"/>
    </linearGradient>
    <linearGradient id="grad80" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f3ff"/>
      <stop offset="66%" stop-color="#8cc0ff"/>
      <stop offset="100%" stop-color="#b8a8ff"/>
    </linearGradient>
    <linearGradient id="grad70" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#5ce1ff"/>
      <stop offset="100%" stop-color="#c89cff"/>
    </linearGradient>
    <linearGradient id="grad60" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8cd4ff"/>
      <stop offset="100%" stop-color="#bc8cff"/>
    </linearGradient>
  </defs>
  
  <text x="400" y="340" text-anchor="middle" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="10" class="text-muted">▲ stack proficiency analysis complete</text>
</svg>'''
    write_svg('section_stack.svg', svg)

def gen_work():
    """ SECTION 4: WORK (Circuit 600x500) """
    svg = '''<svg width="600" height="500" viewBox="0 0 600 500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="card-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#161b22"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
    
    <linearGradient id="ship-glow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#d29922" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#d29922" stop-opacity="0"/>
    </linearGradient>
    
    <linearGradient id="beta-glow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f3ff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#00f3ff" stop-opacity="0"/>
    </linearGradient>
    
    <filter id="glow-gold" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feFlood flood-color="#d29922" flood-opacity="0.5"/>
      <feComposite in2="blur" operator="in"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    
    <filter id="glow-cyan" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feFlood flood-color="#00f3ff" flood-opacity="0.5"/>
      <feComposite in2="blur" operator="in"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    
    <filter id="star-glow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="1" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  
  <style>
    .bg { fill: #0d1117; }
    .bg-light { fill: #f6f8fa; }
    .card-bg { fill: #161b22; stroke: #30363d; stroke-width: 1; }
    .card-bg-light { fill: #ffffff; stroke: #d0d7de; stroke-width: 1; }
    .text-primary { fill: #e6edf3; }
    .text-primary-light { fill: #1f2328; }
    .text-muted { fill: #7d8590; }
    .text-muted-light { fill: #656d76; }
    .text-gold { fill: #d29922; }
    .text-cyan { fill: #00f3ff; }
    .border-line { stroke: #30363d; }
    .border-line-light { stroke: #d0d7de; }
    
    .mono { font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; }
    .project-name { font-family: 'SF Pro Display', -apple-system, sans-serif; font-weight: 700; }
    
    .card-1 { opacity: 0; animation: slideIn 0.6s ease-out 0.2s forwards; }
    .card-2 { opacity: 0; animation: slideIn 0.6s ease-out 0.5s forwards; }
    .card-3 { opacity: 0; animation: slideIn 0.6s ease-out 0.8s forwards; }
    
    @keyframes slideIn {
      0% { opacity: 0; transform: translateX(-30px); }
      100% { opacity: 1; transform: translateX(0); }
    }
    
    .star-icon { animation: twinkle 2s ease-in-out infinite; }
    .star-icon-1 { animation-delay: 0s; }
    .star-icon-2 { animation-delay: 0.3s; }
    .star-icon-3 { animation-delay: 0.6s; }
    
    @keyframes twinkle {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.7; transform: scale(0.9); }
    }
    
    .badge-ship { animation: pulse-gold 2s ease-in-out infinite; }
    .badge-beta { animation: pulse-cyan 2s ease-in-out infinite; }
    
    @keyframes pulse-gold {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.8; }
    }
    
    @keyframes pulse-cyan {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.8; }
    }
    
    .glow-line-ship { animation: glow-pulse-gold 3s ease-in-out infinite; }
    .glow-line-beta { animation: glow-pulse-cyan 3s ease-in-out infinite; }
    
    @keyframes glow-pulse-gold {
      0%, 100% { opacity: 0.3; }
      50% { opacity: 0.7; }
    }
    
    @keyframes glow-pulse-cyan {
      0%, 100% { opacity: 0.3; }
      50% { opacity: 0.7; }
    }
    
    .header-underline { 
      stroke-dasharray: 600; 
      stroke-dashoffset: 600; 
      animation: drawLine 1s ease-out 0.1s forwards; 
    }
    @keyframes drawLine { to { stroke-dashoffset: 0; } }
    
    .cursor-blink { animation: blink 1s step-end infinite; }
    @keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0; } }
    
    @media (prefers-color-scheme: light) {
      .bg { fill: #f6f8fa; }
      .card-bg { fill: #ffffff; stroke: #d0d7de; }
      .text-primary { fill: #1f2328; }
      .text-muted { fill: #656d76; }
      .border-line { stroke: #d0d7de; }
    }
    
    @media (prefers-reduced-motion: reduce) {
      .card-1, .card-2, .card-3 { animation: none; opacity: 1; }
      .star-icon, .badge-ship, .badge-beta { animation: none; }
      .glow-line-ship, .glow-line-beta { animation: none; opacity: 0.5; }
      .header-underline { animation: none; stroke-dashoffset: 0; }
      .cursor-blink { animation: none; opacity: 1; }
    }
  </style>
  
  <rect class="bg" width="600" height="500"/>
  
  <text class="mono" x="30" y="40" font-size="18" font-weight="bold" fill="#58a6ff">
    <tspan fill="#7d8590">$</tspan> ls -la ~/projects/
  </text>
  <rect class="cursor-blink" x="175" y="28" width="8" height="16" fill="#58a6ff"/>
  
  <line class="border-line header-underline" x1="30" y1="55" x2="570" y2="55" stroke-width="1"/>
  
  <g class="mono" font-size="10" fill="#7d8590">
    <text x="30" y="80">PERMISSIONS</text>
    <text x="120" y="80">DOMAIN</text>
    <text x="200" y="80">STARS</text>
    <text x="270" y="80">NAME</text>
    <text x="480" y="80">STATUS</text>
  </g>
  
  <g class="card-1" transform="translate(30, 100)">
    <rect class="card-bg" width="540" height="100" rx="6"/>
    <rect class="glow-line-ship" x="0" y="0" width="4" height="100" rx="2" fill="url(#ship-glow)"/>
    
    <text class="mono" x="20" y="30" font-size="12" fill="#3fb950">drwxr-xr-x</text>
    
    <g transform="translate(120, 18)">
      <rect width="60" height="20" rx="10" fill="#21262d" stroke="#30363d" stroke-width="0.5"/>
      <text class="mono" x="30" y="14" text-anchor="middle" font-size="10" fill="#ff7b72">SecOps</text>
    </g>
    
    <g class="star-icon star-icon-1" transform="translate(200, 15)" filter="url(#star-glow)">
      <polygon points="10,0 12,7 20,7 14,12 16,20 10,15 4,20 6,12 0,7 8,7" fill="#d29922"/>
      <text class="mono" x="28" y="16" font-size="14" font-weight="bold" fill="#d29922">128</text>
    </g>
    
    <text class="project-name" x="270" y="28" font-size="18" fill="#e6edf3">shadow-scripts</text>
    <text class="mono" x="270" y="50" font-size="11" fill="#7d8590">Proxy meshes, DNS overlays, and stealth routing</text>
    
    <g class="badge-ship" transform="translate(480, 15)">
      <rect width="50" height="22" rx="4" fill="#d29922" fill-opacity="0.15" stroke="#d29922" stroke-width="1"/>
      <text class="mono" x="25" y="15" text-anchor="middle" font-size="11" font-weight="bold" fill="#d29922" filter="url(#glow-gold)">SHIP</text>
    </g>
    
    <line x1="20" y1="65" x2="520" y2="65" stroke="#30363d" stroke-width="0.5" stroke-dasharray="4,2"/>
    
    <text class="mono" x="20" y="85" font-size="9" fill="#7d8590">
      <tspan fill="#58a6ff">→</tspan> github.com/Thugger069/shadow-scripts
    </text>
  </g>
  
  <g class="card-2" transform="translate(30, 215)">
    <rect class="card-bg" width="540" height="100" rx="6"/>
    <rect class="glow-line-beta" x="0" y="0" width="4" height="100" rx="2" fill="url(#beta-glow)"/>
    
    <text class="mono" x="20" y="30" font-size="12" fill="#3fb950">drwxr-xr-x</text>
    
    <g transform="translate(120, 18)">
      <rect width="80" height="20" rx="10" fill="#21262d" stroke="#30363d" stroke-width="0.5"/>
      <text class="mono" x="40" y="14" text-anchor="middle" font-size="10" fill="#a371f7">Automation</text>
    </g>
    
    <g class="star-icon star-icon-2" transform="translate(200, 15)" filter="url(#star-glow)">
      <polygon points="10,0 12,7 20,7 14,12 16,20 10,15 4,20 6,12 0,7 8,7" fill="#00f3ff"/>
      <text class="mono" x="28" y="16" font-size="14" font-weight="bold" fill="#00f3ff">245</text>
    </g>
    
    <text class="project-name" x="270" y="28" font-size="18" fill="#e6edf3">smooth-operator</text>
    <text class="mono" x="270" y="50" font-size="11" fill="#7d8590">Siri-driven reply engine with JSON state</text>
    
    <g class="badge-beta" transform="translate(480, 15)">
      <rect width="50" height="22" rx="4" fill="#00f3ff" fill-opacity="0.15" stroke="#00f3ff" stroke-width="1"/>
      <text class="mono" x="25" y="15" text-anchor="middle" font-size="11" font-weight="bold" fill="#00f3ff" filter="url(#glow-cyan)">BETA</text>
    </g>
    
    <line x1="20" y1="65" x2="520" y2="65" stroke="#30363d" stroke-width="0.5" stroke-dasharray="4,2"/>
    
    <text class="mono" x="20" y="85" font-size="9" fill="#7d8590">
      <tspan fill="#58a6ff">→</tspan> github.com/Thugger069/smooth-operator
    </text>
  </g>
  
  <g class="card-3" transform="translate(30, 330)">
    <rect class="card-bg" width="540" height="100" rx="6"/>
    <rect class="glow-line-ship" x="0" y="0" width="4" height="100" rx="2" fill="url(#ship-glow)"/>
    
    <text class="mono" x="20" y="30" font-size="12" fill="#3fb950">drwxr-xr-x</text>
    
    <g transform="translate(120, 18)">
      <rect width="65" height="20" rx="10" fill="#21262d" stroke="#30363d" stroke-width="0.5"/>
      <text class="mono" x="32" y="14" text-anchor="middle" font-size="10" fill="#79c0ff">Surface</text>
    </g>
    
    <g class="star-icon star-icon-3" transform="translate(200, 15)" filter="url(#star-glow)">
      <polygon points="10,0 12,7 20,7 14,12 16,20 10,15 4,20 6,12 0,7 8,7" fill="#d29922"/>
      <text class="mono" x="28" y="16" font-size="14" font-weight="bold" fill="#d29922">89</text>
    </g>
    
    <text class="project-name" x="270" y="28" font-size="18" fill="#e6edf3">brand-terminal</text>
    <text class="mono" x="270" y="50" font-size="11" fill="#7d8590">CLI-style UI skins with real-time telemetry</text>
    
    <g class="badge-ship" transform="translate(480, 15)">
      <rect width="50" height="22" rx="4" fill="#d29922" fill-opacity="0.15" stroke="#d29922" stroke-width="1"/>
      <text class="mono" x="25" y="15" text-anchor="middle" font-size="11" font-weight="bold" fill="#d29922" filter="url(#glow-gold)">SHIP</text>
    </g>
    
    <line x1="20" y1="65" x2="520" y2="65" stroke="#30363d" stroke-width="0.5" stroke-dasharray="4,2"/>
    
    <text class="mono" x="20" y="85" font-size="9" fill="#7d8590">
      <tspan fill="#58a6ff">→</tspan> github.com/Thugger069/brand-terminal
    </text>
  </g>
  
  <text class="mono" x="30" y="470" font-size="10" fill="#7d8590">
    <tspan fill="#3fb950">3 directories</tspan>, <tspan fill="#58a6ff">462 total stars</tspan>
  </text>
  
  <g transform="translate(480, 455)">
    <rect width="90" height="28" rx="4" fill="#21262d" stroke="#30363d"/>
    <text class="mono" x="45" y="18" text-anchor="middle" font-size="10" fill="#7d8590">total 3 proj</text>
  </g>
</svg>'''
    write_svg('section_work.svg', svg)

def gen_telemetry():
    """ SECTION 5: TELEMETRY (Ambient 800x300) """
    svg = '''<svg width="800" height="300" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .mono { font-family: 'Courier New', Consolas, monospace; }
            .header-text { font-size: 14px; font-weight: bold; }
            .label-text { font-size: 11px; }
            .value-text { font-size: 24px; font-weight: bold; }
            .small-value { font-size: 13px; }
            .bar-fill { animation: fillBar 2s ease-out forwards; }
            @keyframes fillBar { from { width: 0; } }
            @keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0; } }
            @keyframes countUp { from { opacity: 0.3; } to { opacity: 1; } }
            .cursor { animation: blink 1s infinite; }
            .value-animate { animation: countUp 0.5s ease-out; }
        </style>
        <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#ff7b72"/>
            <stop offset="100%" stop-color="#d29922"/>
        </linearGradient>
    </defs>

    <rect width="800" height="300" fill="#0d1117"/>
    <rect width="800" height="300" fill="#161b22" style="media (prefers-color-scheme: light)"/>

    <rect x="0" y="0" width="800" height="32" fill="#21262d"/>
    <line x1="0" y1="32" x2="800" y2="32" stroke="#30363d" stroke-width="1"/>

    <circle cx="16" cy="16" r="6" fill="#ff7b72"/>
    <circle cx="36" cy="16" r="6" fill="#d29922"/>
    <circle cx="56" cy="16" r="6" fill="#3fb950"/>

    <text x="400" y="21" text-anchor="middle" class="mono header-text" fill="url(#headerGrad)">GitHub Telemetry Monitor v2.4.1</text>

    <rect x="16" y="48" width="762" height="242" fill="none" stroke="#30363d" stroke-width="1" rx="4"/>
    <rect x="16" y="48" width="762" height="28" fill="#21262d" rx="4"/>
    <rect x="16" y="72" width="762" height="2" fill="#30363d"/>

    <text x="28" y="67" class="mono label-text" fill="#8b949e">METRIC</text>
    <text x="200" y="67" class="mono label-text" fill="#8b949e">VALUE</text>
    <text x="340" y="67" class="mono label-text" fill="#8b949e">STATUS</text>
    <text x="440" y="67" class="mono label-text" fill="#8b949e">METRIC</text>
    <text x="620" y="67" class="mono label-text" fill="#8b949e">VALUE</text>
    <text x="720" y="67" class="mono label-text" fill="#8b949e">STATUS</text>

    <g transform="translate(28, 100)">
        <g transform="translate(0, 0)">
            <path d="M0 6 L4 6 L4 0 L10 0 L10 6 L14 6 L7 14 Z" fill="#3fb950"/>
            <text x="22" y="12" class="mono label-text" fill="#c9d1d9">COMMITS</text>
            <text x="172" y="12" class="mono value-text value-animate" fill="#3fb950">
                <tspan>2847</tspan>
                <animate attributeName="opacity" values="0;1" dur="1.5s" fill="freeze"/>
            </text>
            <rect x="298" y="2" width="40" height="14" fill="#238636" rx="2"/>
            <text x="318" y="12" text-anchor="middle" class="mono label-text" fill="#fff">HEALTHY</text>
        </g>

        <g transform="translate(0, 42)">
            <path d="M7 0 L10 5 L7 10 L4 5 Z M0 10 L3 5 L0 0 L7 0 L14 0 L11 5 L14 10 Z" fill="#ff7b72" transform="translate(0, 2) scale(1)"/>
            <text x="22" y="12" class="mono label-text" fill="#c9d1d9">REPOSITORIES</text>
            <text x="172" y="12" class="mono value-text value-animate" fill="#ff7b72">
                <tspan>23</tspan>
                <animate attributeName="opacity" values="0;1" dur="1.2s" fill="freeze"/>
            </text>
            <rect x="298" y="2" width="40" height="14" fill="#9e6a03" rx="2"/>
            <text x="318" y="12" text-anchor="middle" class="mono label-text" fill="#fff">ACTIVE</text>
        </g>

        <g transform="translate(0, 84)">
            <path d="M7 0 L9 5 L14 6 L10 9 L11 14 L7 11 L3 14 L4 9 L0 6 L5 5 Z" fill="#d29922"/>
            <text x="22" y="12" class="mono label-text" fill="#c9d1d9">STARS EARNED</text>
            <text x="172" y="12" class="mono value-text value-animate" fill="#d29922">
                <tspan>462</tspan>
                <animate attributeName="opacity" values="0;1" dur="1.8s" fill="freeze"/>
            </text>
            <rect x="298" y="2" width="40" height="14" fill="#238636" rx="2"/>
            <text x="318" y="12" text-anchor="middle" class="mono label-text" fill="#fff">RISING</text>
        </g>
    </g>

    <g transform="translate(412, 100)">
        <g transform="translate(0, 0)">
            <path d="M2 0 L12 0 C13 0 14 1 14 2 L14 8 C14 9 13 10 12 10 L9 10 L7 13 L5 10 L2 10 C1 10 0 9 0 8 L0 2 C0 1 1 0 2 0" fill="#58a6ff"/>
            <text x="22" y="12" class="mono label-text" fill="#c9d1d9">PULL REQUESTS</text>
            <text x="188" y="12" class="mono value-text value-animate" fill="#58a6ff">
                <tspan>156</tspan>
                <animate attributeName="opacity" values="0;1" dur="1.4s" fill="freeze"/>
            </text>
            <rect x="288" y="2" width="40" height="14" fill="#238636" rx="2"/>
            <text x="308" y="12" text-anchor="middle" class="mono label-text" fill="#fff">MERGED</text>
        </g>

        <g transform="translate(0, 42)">
            <circle cx="7" cy="7" r="7" fill="none" stroke="#f778ba" stroke-width="2"/>
            <path d="M7 4 L7 7 L9 9" stroke="#f778ba" stroke-width="2" fill="none"/>
            <text x="22" y="12" class="mono label-text" fill="#c9d1d9">ISSUES CLOSED</text>
            <text x="188" y="12" class="mono value-text value-animate" fill="#f778ba">
                <tspan>89</tspan>
                <animate attributeName="opacity" values="0;1" dur="1.6s" fill="freeze"/>
            </text>
            <rect x="288" y="2" width="40" height="14" fill="#238636" rx="2"/>
            <text x="308" y="12" text-anchor="middle" class="mono label-text" fill="#fff">SOLVED</text>
        </g>

        <g transform="translate(0, 84)">
            <path d="M0 3 L7 3 L7 0 L14 5 L7 10 L7 7 L0 7 Z" fill="#7ee787"/>
            <path d="M14 3 L7 3 L7 0 L0 5 L7 10 L7 7 L14 7 Z" fill="#7ee787" opacity="0.5" transform="translate(2, 0)"/>
            <text x="22" y="12" class="mono label-text" fill="#c9d1d9">CODE REVIEWS</text>
            <text x="188" y="12" class="mono value-text value-animate" fill="#7ee787">
                <tspan>234</tspan>
                <animate attributeName="opacity" values="0;1" dur="2s" fill="freeze"/>
            </text>
            <rect x="288" y="2" width="40" height="14" fill="#238636" rx="2"/>
            <text x="308" y="12" text-anchor="middle" class="mono label-text" fill="#fff">APPROVED</text>
        </g>
    </g>

    <line x1="396" y1="82" x2="396" y2="282" stroke="#30363d" stroke-width="1"/>

    <rect x="16" y="252" width="762" height="26" fill="#21262d" rx="0 0 4 4"/>
    <line x1="16" y1="252" x2="778" y2="252" stroke="#30363d"/>

    <text x="28" y="269" class="mono label-text" fill="#8b949e">UPTIME:</text>
    <text x="88" y="269" class="mono small-value" fill="#3fb950">99.97%</text>

    <text x="170" y="269" class="mono label-text" fill="#8b949e">LAST SYNC:</text>
    <text x="248" y="269" class="mono small-value" fill="#c9d1d9">2026-02-17T08:42:16Z</text>

    <text x="480" y="269" class="mono label-text" fill="#8b949e">STATUS:</text>
    <circle cx="540" cy="265" r="4" fill="#3fb950">
        <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="552" y="269" class="mono small-value" fill="#3fb950">LIVE</text>

    <text x="620" y="269" class="mono label-text" fill="#8b949e">REFRESH:</text>
    <text x="688" y="269" class="mono small-value" fill="#d29922">30s</text>

    <rect class="cursor" x="716" y="258" width="8" height="14" fill="#ff7b72"/>
</svg>
'''
    write_svg('section_telemetry.svg', svg)

def gen_security():
    """ SECTION 6: SECURITY (Stripes 1000x40) """
    svg = '''<svg width="1000" height="120" viewBox="0 0 1000 120" xmlns="http://www.w3.org/2000/svg">
  <style>
    @keyframes logFade1 {
      0%, 14% { opacity: 0; }
      15%, 100% { opacity: 1; }
    }
    @keyframes logFade2 {
      0%, 29% { opacity: 0; }
      30%, 100% { opacity: 1; }
    }
    @keyframes logFade3 {
      0%, 44% { opacity: 0; }
      45%, 100% { opacity: 1; }
    }
    @keyframes logFade4 {
      0%, 59% { opacity: 0; }
      60%, 100% { opacity: 1; }
    }
    @keyframes cursorBlink {
      0%, 50% { opacity: 1; }
      51%, 100% { opacity: 0; }
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.6; }
    }
    .log-entry-1 { animation: logFade1 4s ease-out forwards; }
    .log-entry-2 { animation: logFade2 4s ease-out forwards; }
    .log-entry-3 { animation: logFade3 4s ease-out forwards; }
    .log-entry-4 { animation: logFade4 4s ease-out forwards; }
    .cursor { animation: cursorBlink 1s step-end infinite; }
    .status-pulse { animation: pulse 2s ease-in-out infinite; }
    @media (prefers-color-scheme: light) {
      .bg { fill: #f6f8fa; }
      .log-text { fill: #24292f; }
      .timestamp { fill: #57606a; }
      .status-ok { fill: #1a7f37; }
      .border { stroke: #d0d7de; }
      .header-bg { fill: #eaeef2; }
      .cursor-char { fill: #24292f; }
    }
    @media (prefers-color-scheme: dark) {
      .bg { fill: #0d1117; }
      .log-text { fill: #c9d1d9; }
      .timestamp { fill: #6e7681; }
      .status-ok { fill: #3fb950; }
      .border { stroke: #30363d; }
      .header-bg { fill: #161b22; }
      .cursor-char { fill: #c9d1d9; }
    }
  </style>
  
  <rect class="bg" width="1000" height="120" rx="0"/>
  
  <rect class="header-bg" x="0" y="0" width="1000" height="24" rx="0"/>
  <line class="border" x1="0" y1="24" x2="1000" y2="24" stroke-width="1"/>
  
  <g transform="translate(16, 16)">
    <circle cx="0" cy="0" r="5" fill="#ff5f56"/>
    <circle cx="14" cy="0" r="5" fill="#ffbd2e"/>
    <circle cx="28" cy="0" r="5" fill="#27c93f"/>
  </g>
  
  <text x="500" y="16" text-anchor="middle" font-family="'SF Mono', 'Fira Code', 'Consolas', monospace" font-size="11" class="log-text" opacity="0.7">system://popdeuxrem/security-logs</text>

  <g font-family="'SF Mono', 'Fira Code', 'Consolas', monospace" font-size="13">
    <g class="log-entry-1" opacity="0">
      <text x="20" y="48" class="timestamp">[2026-02-17 08:00:00]</text>
      <text x="195" y="48" class="log-text">SECURITY_SCAN:</text>
      <text x="315" y="48" class="status-ok" font-weight="600">✓ PASSED</text>
      <circle cx="380" cy="44" r="3" class="status-ok status-pulse"/>
    </g>
    
    <g class="log-entry-2" opacity="0">
      <text x="20" y="68" class="timestamp">[2026-02-17 08:00:01]</text>
      <text x="195" y="68" class="log-text">DEPENDENCY_AUDIT:</text>
      <text x="345" y="68" class="status-ok" font-weight="600">✓ CLEAN</text>
      <rect x="400" y="56" width="10" height="10" rx="2" fill="none" class="status-ok" stroke-width="1.5"/>
      <path d="M402 61 L405 64 L408 58" stroke="currentColor" class="status-ok" stroke-width="1.5" fill="none"/>
    </g>
    
    <g class="log-entry-3" opacity="0">
      <text x="20" y="88" class="timestamp">[2026-02-17 08:00:02]</text>
      <text x="195" y="88" class="log-text">BUILD_SIG:</text>
      <text x="285" y="88" class="status-ok" font-weight="500">SHA256:a3f8c9d2</text>
      <rect x="395" y="78" width="60" height="14" rx="3" class="status-ok" fill="none" stroke-width="1" opacity="0.5"/>
      <text x="400" y="89" font-size="9" class="status-ok" opacity="0.7">VERIFIED</text>
    </g>
    
    <g class="log-entry-4" opacity="0">
      <text x="20" y="108" class="timestamp">[2026-02-17 08:00:03]</text>
      <text x="195" y="108" class="log-text">SURFACE_STATUS:</text>
      <text x="330" y="108" class="status-ok" font-weight="600">OPERATIONAL</text>
    </g>
  </g>
  
  <g class="log-entry-4" opacity="0">
    <text x="440" y="108" font-family="'SF Mono', 'Fira Code', 'Consolas', monospace" font-size="13" class="cursor-char cursor">▌</text>
  </g>
  
  <g transform="translate(920, 98)">
    <rect x="0" y="0" width="60" height="16" rx="4" class="status-ok" fill="none" stroke-width="1.5" opacity="0.4"/>
    <text x="30" y="12" text-anchor="middle" font-family="'SF Mono', 'Fira Code', 'Consolas', monospace" font-size="9" class="status-ok" font-weight="600">SECURE</text>
    <circle cx="8" cy="8" r="3" class="status-ok status-pulse"/>
  </g>
</svg>
'''
    write_svg('section_security.svg', svg)

def gen_quote():
    """ SECTION 7: QUOTE (Particle emanation 800x150) """
    with open('data/quotes.json', 'r') as f:
        quotes = json.load(f)
    quote = random.choice(quotes)
    text = quote['text']
    author = quote['author']
    
    svg = f'''<svg width="800" height="150" viewBox="0 0 800 150" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="quote-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="50%" stop-color="#161b22"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
    <linearGradient id="particle-rise" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#f0883e" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#f0883e" stop-opacity="0"/>
    </linearGradient>
    <filter id="particle-blur">
      <feGaussianBlur stdDeviation="0.8"/>
    </filter>
    <filter id="quote-glow">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <style>
    .bg-dark {{ fill: #0d1117; }}
    .quote-text {{ 
      font-family: Georgia, 'Times New Roman', serif; 
      font-size: 18px; 
      font-style: italic;
      fill: #e6edf3;
    }}
    .author-text {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 12px;
      font-weight: 500;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      fill: #f0883e;
    }}
    .quote-mark {{
      fill: #30363d;
      opacity: 0.25;
    }}
    .edge-particle {{
      fill: #f0883e;
      opacity: 0;
    }}
    .particle-up-1 {{ animation: rise-1 4s ease-out infinite; }}
    .particle-up-2 {{ animation: rise-2 5s ease-out infinite; }}
    .particle-up-3 {{ animation: rise-3 6s ease-out infinite; }}
    .particle-up-4 {{ animation: rise-4 4.5s ease-out infinite; }}
    .particle-up-5 {{ animation: rise-5 5.5s ease-out infinite; }}
    .particle-up-6 {{ animation: rise-6 3.8s ease-out infinite; }}
    .particle-up-7 {{ animation: rise-7 5.2s ease-out infinite; }}
    .particle-up-8 {{ animation: rise-8 4.2s ease-out infinite; }}
    .particle-up-9 {{ animation: rise-9 6.2s ease-out infinite; }}
    .particle-up-10 {{ animation: rise-10 5s ease-out infinite; }}
    @keyframes rise-1 {{
      0% {{ opacity: 0; transform: translate(0, 0) scale(1); }}
      20% {{ opacity: 0.7; }}
      100% {{ opacity: 0; transform: translate(-15px, -80px) scale(0.3); }}
    }}
    @keyframes rise-2 {{
      0% {{ opacity: 0; transform: translate(0, 0) scale(1); }}
      15% {{ opacity: 0.6; }}
      100% {{ opacity: 0; transform: translate(10px, -90px) scale(0.2); }}
    }}
    @keyframes rise-3 {{
      0% {{ opacity: 0; transform: translate(0, 0) scale(1); }}
      25% {{ opacity: 0.8; }}
      100% {{ opacity: 0; transform: translate(-8px, -75px) scale(0.4); }}
    }}
    @keyframes rise-4 {{
      0% {{ opacity: 0; transform: translate(0, 0) scale(1); }}
      30% {{ opacity: 0.5; }}
      100% {{ opacity: 0; transform: translate(20px, -85px) scale(0.25); }}
    }}
    @keyframes rise-5 {{
      0% {{ opacity: 0; transform: translate(0, 0) scale(1); }}
      20% {{ opacity: 0.65; }}
      100% {{ opacity: 0; transform: translate(-12px, -95px) scale(0.35); }}
    }}
    @keyframes rise-6 {{
      0% {{ opacity: 0; transform: translate(0, 0) scale(1); }}
      15% {{ opacity: 0.55; }}
      100% {{ opacity: 0; transform: translate(5px, -70px) scale(0.45); }}
    }}
    @keyframes rise-7 {{
      0% {{ opacity: 0; transform: translate(0, 0) scale(1); }}
      25% {{ opacity: 0.75; }}
      100% {{ opacity: 0; transform: translate(-18px, -88px) scale(0.28); }}
    }}
    @keyframes rise-8 {{
      0% {{ opacity: 0; transform: translate(0, 0) scale(1); }}
      20% {{ opacity: 0.6; }}
      100% {{ opacity: 0; transform: translate(12px, -78px) scale(0.38); }}
    }}
    @keyframes rise-9 {{
      0% {{ opacity: 0; transform: translate(0, 0) scale(1); }}
      30% {{ opacity: 0.5; }}
      100% {{ opacity: 0; transform: translate(-6px, -92px) scale(0.22); }}
    }}
    @keyframes rise-10 {{
      0% {{ opacity: 0; transform: translate(0, 0) scale(1); }}
      15% {{ opacity: 0.7; }}
      100% {{ opacity: 0; transform: translate(16px, -82px) scale(0.32); }}
    }}
    .quote-reveal {{
      opacity: 0;
      animation: quote-fade 1.2s ease-out 0.3s forwards;
    }}
    @keyframes quote-fade {{
      0% {{ opacity: 0; transform: translateY(10px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .accent-line {{
      stroke: #f0883e;
      stroke-width: 1;
      opacity: 0;
      animation: line-reveal 1s ease-out 0.8s forwards;
    }}
    @keyframes line-reveal {{
      0% {{ opacity: 0; stroke-dashoffset: 100; }}
      100% {{ opacity: 0.4; stroke-dashoffset: 0; }}
    }}
    @media (prefers-color-scheme: light) {{
      .bg-dark {{ fill: #f6f8fa; }}
      .quote-text {{ fill: #1f2328; }}
      .author-text {{ fill: #bd561d; }}
      .quote-mark {{ fill: #d0d7de; }}
      .edge-particle {{ fill: #bd561d; }}
      .accent-line {{ stroke: #bd561d; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .particle-up-1, .particle-up-2, .particle-up-3, .particle-up-4,
      .particle-up-5, .particle-up-6, .particle-up-7, .particle-up-8,
      .particle-up-9, .particle-up-10 {{ animation: none; opacity: 0.3; }}
      .quote-reveal, .accent-line {{ animation: none; opacity: 1; }}
    }}
  </style>
  <rect class="bg-dark" width="800" height="150"/>
  <g filter="url(#particle-blur)">
    <circle class="edge-particle particle-up-1" cx="50" cy="130" r="3"/>
    <circle class="edge-particle particle-up-2" cx="75" cy="140" r="2"/>
    <circle class="edge-particle particle-up-3" cx="100" cy="125" r="2.5"/>
    <circle class="edge-particle particle-up-4" cx="700" cy="135" r="2"/>
    <circle class="edge-particle particle-up-5" cx="725" cy="128" r="3"/>
    <circle class="edge-particle particle-up-6" cx="750" cy="140" r="2"/>
    <circle class="edge-particle particle-up-7" cx="45" cy="145" r="1.5"/>
    <circle class="edge-particle particle-up-8" cx="755" cy="142" r="1.5"/>
    <circle class="edge-particle particle-up-9" cx="125" cy="138" r="2"/>
    <circle class="edge-particle particle-up-10" cx="680" cy="132" r="2.5"/>
  </g>
  <g opacity="0.15">
    <text class="quote-mark" x="140" y="95" font-family="Georgia, serif" font-size="120">"</text>
    <text class="quote-mark" x="620" y="95" font-family="Georgia, serif" font-size="120">"</text>
  </g>
  <line class="accent-line" x1="200" y1="50" x2="600" y2="50" stroke-dasharray="100"/>
  <g class="quote-reveal">
    <text class="quote-text" x="400" y="80" text-anchor="middle">"{text}"</text>
    <text class="author-text" x="400" y="108" text-anchor="middle" filter="url(#quote-glow)">— {author}</text>
  </g>
  <line class="accent-line" x1="250" y1="120" x2="550" y2="120" stroke-dasharray="100"/>
  <g opacity="0.08">
    <rect x="0" y="0" width="800" height="1" fill="#f0883e"/>
    <rect x="0" y="149" width="800" height="1" fill="#f0883e"/>
  </g>
</svg>'''
    write_svg('section_quote.svg', svg)
