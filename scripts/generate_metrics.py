import datetime
import os

def generate_skill_matrix():
    # Simulated data derived from repository telemetry
    skills = {
        "Orchestration": 95,
        "Automation": 98,
        "Security": 88,
        "Architecture": 92,
        "Full-Stack": 85
    }
    
    matrix = "```text\n"
    matrix += "◈ SYSTEM CAPABILITY MATRIX ◈\n"
    matrix += "--------------------------------------\n"
    for skill, value in skills.items():
        bar_length = int(value / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        matrix += f"{skill:<15} [{bar}] {value}%\n"
    matrix += "--------------------------------------\n"
    matrix += "```"
    return matrix

def get_system_uptime():
    # Career epoch: Oct 2025 (Based on profile context)
    epoch = datetime.datetime(2025, 10, 27)
    now = datetime.datetime.now()
    diff = now - epoch
    
    days = diff.days
    hours = diff.seconds // 3600
    return f"{days}D {hours}H"

def main():
    # Validate Output Directory
    if not os.path.exists('dist'):
        os.makedirs('dist')

    metrics = {
        "SKILL_MATRIX": generate_skill_matrix(),
        "UPTIME": get_system_uptime(),
        "LAST_SYNC": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "STATUS": "NOMINAL"
    }

    # Generate flat-file telemetry for the updater script to consume
    with open('dist/telemetry.env', 'w') as f:
        for key, value in metrics.items():
            # Handle multi-line strings for shell sourcing
            if "\n" in str(value):
                f.write(f'{key}="{value}"\n')
            else:
                f.write(f'{key}={value}\n')

if __name__ == "__main__":
    main()
