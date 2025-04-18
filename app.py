import streamlit as st
from pathlib import Path
from upload_utils import extract_and_save_files
from log_writer import append_log
import base64

st.set_page_config(page_title="Chat Agent File Assistant", layout="wide")
st.title("📁 GPT File Assistant with GitHub Sync")

project = st.text_input("Project Name (folder will be created if it doesn't exist)", "snp-expansion")
project_dir = Path("projects") / project
project_dir.mkdir(parents=True, exist_ok=True)

st.markdown("---")

# 📂 Upload Actual Files section
st.subheader("📂 Upload Actual Files")
uploaded_files = st.file_uploader("Drop your .csv, .toml, or .zip files here", type=["csv", "toml", "zip"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = project_dir / uploaded_file.name
        file_path.write_bytes(uploaded_file.getvalue())
        st.success(f"✅ Saved: {uploaded_file.name}")

        # Log action
        append_log(project_dir, f"Uploaded file: {uploaded_file.name}", "Saved via upload zone")

    st.info("All uploaded files have been saved and committed.")
    st.balloons()

# 📋 Paste GPT block
st.subheader("📋 Paste Full File from GPT")
pasted_text = st.text_area("Paste your GPT-generated file block (include filename header and triple backticks)", height=300)

if st.button("✅ Save Pasted File") and pasted_text:
    try:
        filename, content = extract_and_save_files(pasted_text, project_dir)
        if filename:
            st.success(f"Saved and committed: {filename}")
            append_log(project_dir, pasted_text, f"Saved via paste panel: {filename}")
    except Exception as e:
        st.error(f"Error: {e}")