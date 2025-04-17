import streamlit as st
from pathlib import Path
import os
from agent import process_file
from upload_utils import extract_and_save_files
from log_writer import append_log
from dna_generator import generate_snp_file

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Chat Agent Paste Panel", layout="centered")
st.title("🧬 GPT Project File Assistant with Auto GitHub Push")

project_name = st.text_input("Project folder name:", value="dna-project")
project_dir = PROJECTS_DIR / project_name
project_dir.mkdir(parents=True, exist_ok=True)

st.markdown("---")

# Paste Panel
st.header("📋 Paste Full File from GPT")
pasted_text = st.text_area("Paste your GPT-generated file block (include filename header and triple backticks)", height=300)
if st.button("✅ Save Pasted File"):
    if pasted_text.strip():
        saved_files = extract_and_save_files(pasted_text, project_dir)
        if saved_files:
            st.success(f"Saved and pushed {len(saved_files)} file(s): " + ", ".join(saved_files))
        else:
            st.error("❌ No valid files found in pasted input.")
    else:
        st.warning("Paste area is empty.")

# DNA Generation Buttons
st.markdown("---")
st.header("🧬 Generate New SNP Data")

col1, col2 = st.columns(2)
with col1:
    if st.button("🧬 Generate Nutrigenomics SNPs"):
        content = generate_snp_file("nutrigenomics")
        filename = "nutrigenomics.csv"
        unique_content = filter_new_rsids(content, project_dir)
        process_file(filename, unique_content, project_dir)
        append_log(project_dir, "Generated nutrigenomics SNPs", unique_content)
        st.success(f"Generated and saved: {filename}")

with col2:
    if st.button("💊 Generate Pharmacogenomics SNPs"):
        content = generate_snp_file("pharmacogenomics")
        filename = "pharmacogenomics.csv"
        unique_content = filter_new_rsids(content, project_dir)
        process_file(filename, unique_content, project_dir)
        append_log(project_dir, "Generated pharmacogenomics SNPs", unique_content)
        st.success(f"Generated and saved: {filename}")

# Utility to filter new rsIDs
def filter_new_rsids(csv_text, project_dir):
    seen_file = project_dir / "seen_rsids.txt"
    seen_rsids = set()
    if seen_file.exists():
        seen_rsids = set(seen_file.read_text(encoding="utf-8").splitlines())

    lines = csv_text.strip().splitlines()
    header = lines[0]
    new_lines = [header]
    new_rsids = []

    for line in lines[1:]:
        parts = line.strip().split(",")
        if not parts or len(parts) < 1:
            continue
        rsid = parts[0]
        if rsid not in seen_rsids:
            new_lines.append(line)
            new_rsids.append(rsid)

    # Save new rsIDs
    with open(seen_file, "a", encoding="utf-8") as f:
        for rsid in new_rsids:
            f.write(rsid + "\n")

    return "\n".join(new_lines)