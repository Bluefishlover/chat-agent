from pathlib import Path
from datetime import datetime

def append_log(project_dir: Path, prompt: str, response: str):
    log_path = project_dir / "chatlog.md"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"### {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("**Prompt or Source:**\n```\n")
        f.write(prompt.strip())
        f.write("\n```\n")
        f.write("**Response or Code:**\n```\n")
        f.write(response.strip())
        f.write("\n```\n\n")