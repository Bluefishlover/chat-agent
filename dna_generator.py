import openai

def generate_snp_file(domain):
    prompt = f"Generate a CSV of 100 SNPs related to {domain}. Format as: rsid,gene,trait,impact"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    content = response['choices'][0]['message']['content'].strip()
    return content