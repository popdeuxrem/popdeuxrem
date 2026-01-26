import json
from pathlib import Path
import matplotlib.pyplot as plt

def plot_timeline(output_path: Path):
    if not Path('timeline.json').exists(): return
    with open('timeline.json') as f:
        entries = json.load(f)
    
    techs = [e['technology'] for e in entries]
    years = [e['year'] for e in entries]
    
    BG = '#0D1117'
    TEXT = '#C9D1D9'
    BAR = '#238636'
    
    fig, ax = plt.subplots(figsize=(8, 0.5 * len(entries)))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    
    y_pos = range(len(entries))
    min_year = min(years) - 0.5
    vals = [y - min_year for y in years]
    
    bars = ax.barh(y_pos, vals, color=BAR, height=0.4)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(techs, fontfamily="monospace", color=TEXT)
    ax.invert_yaxis()
    
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.set_xticks([])
    ax.tick_params(left=False, bottom=False)
    
    for bar, year in zip(bars, years):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                f"[{year}]", va='center', color=TEXT, fontfamily="monospace")
                
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path, dpi=100, bbox_inches='tight', facecolor=BG)

if __name__ == "__main__":
    plot_timeline(Path('dist/technology-timeline.png'))
