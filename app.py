
import streamlit as st
from agent import chat_with_agent
from github_utils import commit_and_push

st.set_page_config(page_title="AI Project Assistant", layout="wide")

st.title("🤖 Auto-Saving AI Project Assistant")
prompt = st.text_area("Enter your command", height=150)

if st.button("Submit"):
    if prompt:
        response = chat_with_agent(prompt)
        st.code(response, language="python")

if st.button("Push to GitHub"):
    commit_message = st.text_input("Commit message", "Update project files")
    if commit_message:
        result = commit_and_push(commit_message)
        st.success(result)
