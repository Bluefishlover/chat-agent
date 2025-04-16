from pathlib import Path
from datetime import datetime

def append_log(project_dir, prompt, response):
    log_path = project_dir / "chatlog.md"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n### {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Prompt or Source:** {prompt}\n\n")
        f.write("**Response or Code:**\n```\n")
        f.write(response)
        f.write("\n```\n")
