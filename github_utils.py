
import os
import subprocess

def commit_and_push(message):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)
        return "✅ Changes committed and pushed to GitHub!"
    except subprocess.CalledProcessError as e:
        return f"❌ Git error: {e}"
