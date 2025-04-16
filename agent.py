
import openai
import os
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_agent(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    content = response.choices[0].message['content']
    filename = "output.py"
    lines = prompt.lower().split("\n")
    for line in lines:
        if "file called" in line and ".py" in line:
            filename = line.split("file called")[-1].strip().replace('"','').replace("'", "")
            break
    return filename, content

def extract_filename_and_code(text):
    lines = text.strip().splitlines()
    filename = None
    code_lines = []
    inside_code = False
    for line in lines:
        if "filename:" in line.lower():
            filename = line.split(":")[-1].strip()
        elif line.strip().startswith("```"):
            if inside_code:
                break
            else:
                inside_code = True
        elif inside_code:
            code_lines.append(line)
    code = "\n".join(code_lines)
    return filename, code
