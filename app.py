
import streamlit as st
from agent import chat_with_agent, extract_filename_and_code
from github_utils import auto_commit_and_push, auto_pull
from log_writer import append_log
from pathlib import Path

st.set_page_config(page_title="Auto-Saving GPT Assistant", layout="wide")
st.title("🤖 ChatGPT Assistant with Auto-Push, Pull, Logging & Paste Panel")

project = st.text_input("Project name", value="default")
project_dir = Path("projects") / project
project_dir.mkdir(parents=True, exist_ok=True)

auto_pull(project_dir)

st.header("💬 AI Prompt")
prompt = st.text_area("Enter a task for the AI", height=150)

if st.button("Submit"):
    if prompt.strip():
        filename, content = chat_with_agent(prompt)
        if filename and content:
            file_path = project_dir / filename
            file_path.write_text(content, encoding="utf-8")
            append_log(project_dir, prompt, content)
            result = auto_commit_and_push(filename, project)
            st.success(f"{filename} saved and pushed to GitHub!")
            st.code(content, language="python")
        else:
            st.warning("No file was generated.")

st.header("📋 Paste Full File from GPT")
paste_input = st.text_area("Paste file block (including filename)", height=200)

if st.button("Save Pasted File"):
    if paste_input.strip():
        filename, code = extract_filename_and_code(paste_input)
        if filename and code:
            file_path = project_dir / filename
            file_path.write_text(code, encoding="utf-8")
            append_log(project_dir, f"PASTED: {filename}", code)
            result = auto_commit_and_push(filename, project)
            st.success(f"{filename} saved and pushed to GitHub!")
            st.code(code, language="python")
        else:
            st.error("Could not detect filename or code.")
