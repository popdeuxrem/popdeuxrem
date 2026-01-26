import json
import math
from pathlib import Path
import matplotlib.pyplot as plt

def create_radar_chart(output_path: Path):
    if not Path('skills.json').exists(): return
    with open('skills.json') as f:
        data = json.load(f)
    skills = [(x['name'].upper(), x['score']) for x in data['skills']]
    labels = [x[0] for x in skills] + [skills[0][0]]
    scores = [x[1] for x in skills] + [skills[0][1]]
    
    angles = [n / float(len(skills)) * 2 * math.pi for n in range(len(skills))]
    angles += angles[:1]
    
    BG = '#0D1117'
    ACCENT = '#00FF9D'
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)
    
    plt.xticks(angles[:-1], labels[:-1], color='#8B949E', size=9, fontfamily='monospace', weight='bold')
    ax.set_yticklabels([])
    ax.spines['polar'].set_visible(False)
    ax.grid(color='#30363D')
    
    ax.plot(angles, scores, color=ACCENT, linewidth=2)
    ax.fill(angles, scores, color=ACCENT, alpha=0.15)
    
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path, dpi=100, bbox_inches='tight', facecolor=BG)

if __name__ == "__main__":
    create_radar_chart(Path('dist/skills-radar.png'))
