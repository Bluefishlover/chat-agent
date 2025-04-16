
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_agent(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message['content']
