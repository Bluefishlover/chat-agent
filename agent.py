import os
import subprocess
from pathlib import Path

def process_file(filename: str, content: str, project_dir: Path):
    """Save file and push to GitHub"""
    filepath = project_dir / filename
    filepath.write_text(content, encoding="utf-8")

    # Git add, commit, push
    try:
        subprocess.run(["git", "add", str(filepath)], check=True)
        subprocess.run(["git", "commit", "-m", f"Add {filename}"], check=True)
        subprocess.run(["git", "push"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}")