import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def mock_network(output_path: Path):
    BG = '#0D1117'
    NODE = '#00BFFF'
    
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    
    # Generate random constellation
    np.random.seed(42)
    x = np.random.rand(20)
    y = np.random.rand(20)
    
    for i in range(20):
        for j in range(i+1, 20):
            if np.random.rand() > 0.85:
                ax.plot([x[i], x[j]], [y[i], y[j]], color='#30363D', linewidth=0.5)
                
    ax.scatter(x, y, color=NODE, s=50, alpha=0.8)
    ax.scatter([0.5], [0.5], color='#E6EDF3', s=100, zorder=10) # Self
    
    ax.axis('off')
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path, dpi=100, bbox_inches='tight', facecolor=BG)

if __name__ == "__main__":
    mock_network(Path('dist/network-graph.png'))
