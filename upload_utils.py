import zipfile
from io import StringIO
import streamlit as st
from agent import process_file

def extract_and_save_files(input_data, project_dir, is_uploaded=False):
    saved_files = []

    if is_uploaded:
        if input_data.name.endswith(".zip"):
            with zipfile.ZipFile(input_data, "r") as zip_ref:
                for name in zip_ref.namelist():
                    with zip_ref.open(name) as f:
                        content = f.read().decode("utf-8")
                        process_file(name, content, project_dir)
                        saved_files.append(name)
        elif input_data.name.endswith(".txt"):
            bundle_text = input_data.read().decode("utf-8")
            saved_files = parse_bundle_text(bundle_text, project_dir)
    else:
        saved_files = parse_bundle_text(input_data, project_dir)

    return saved_files

def parse_bundle_text(text, project_dir):
    files = []
    blocks = text.split("### 📄 Filename:")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        filename = lines[0].strip()
        try:
            code_start = next(i for i, line in enumerate(lines) if line.strip().startswith("```"))
            code_lines = []
            for line in lines[code_start+1:]:
                if line.strip().startswith("```"):
                    break
                code_lines.append(line)
            content = "\n".join(code_lines)
            process_file(filename, content, project_dir)
            files.append(filename)
        except Exception as e:
            st.error(f"❌ Error processing {filename}: {e}")
    return files