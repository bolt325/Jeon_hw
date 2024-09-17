import openai
import os
import PyPDF2

# >>>>> API 키 입력 <<<<<
openai.api_key = "API_KEY"

def extract_text(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def translate_paper(paper_text, target_language="ko"):
    prompt = f"다음 논문을 {target_language}로 번역해 주세요:\n\n{paper_text}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are professional traslator, and you can speak korean very frequently."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2000,
        temperature=0.5
    )
    translation = response['choices'][0]['message']['content'].strip()
    return translation

def summarize_paper(paper_text):
    prompt = f"다음 논문을 요약해 주세요:\n\n{paper_text}\n\n요약:"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional paper analyst."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.5
    )
    summary = response['choices'][0]['message']['content'].strip()
    return summary

def extract(paper_text):
    prompt = f"다음 논문에서 사용된 중요한 공식과 주제를 찾아주세요:\n\n{paper_text}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional paper analyst, and critic."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.5,
    )
    important = response['choices'][0]['message']['content'].strip()
    return important

# >>>>> PDF 파일 경로 입력 <<<<<
pdf_path = "PATH FOR TARGET FILE"

paper_text = extract_text(pdf_path)
summary = summarize_paper(paper_text)
translated_text = translate_paper(paper_text, target_language="ko")
important_parts = extract(paper_text)

print("논문 요약:")
print(summary)
print("\n번역된 논문:")
print(translated_text)
print("\n중요한 부분:")
print(important_parts)