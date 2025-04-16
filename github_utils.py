
import subprocess
from pathlib import Path

def auto_commit_and_push(filename, project):
    file_path = Path("projects") / project / filename
    try:
        subprocess.run(["git", "add", str(file_path)], check=True)
        subprocess.run(["git", "commit", "-m", f'Auto-save and push: {project}/{filename}'], check=True)
        subprocess.run(["git", "push"], check=True)
        return f"{filename} committed and pushed."
    except subprocess.CalledProcessError as e:
        return f"Git error: {e}"

def auto_pull(project_path):
    try:
        subprocess.run(["git", "pull"], cwd=str(Path.cwd()), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Git pull failed: {e}")
