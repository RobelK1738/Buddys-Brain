import os
import json
from openai import OpenAI
import tiktoken
from dotenv import load_dotenv

load_dotenv(dotenv_path='../../../.env')
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o"
MAX_INPUT_TOKENS = 100_000
MAX_OUTPUT_TOKENS = 500

def load_json(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def tokenize_count(text: str) -> int:
    enc = tiktoken.encoding_for_model(MODEL)
    return len(enc.encode(text))

def summarize_resources(json_data, query: str) -> str:
    summaries = [resource['summary'] for resource in json_data]
    combined_summaries = " ".join(summaries)
    token_count = tokenize_count(combined_summaries)

    if token_count > MAX_INPUT_TOKENS:
        raise ValueError(f"Input data too large to process in one shot (>{MAX_INPUT_TOKENS} tokens).")

    prompt = (
        f"Given the following educational resource summaries:\n{combined_summaries}\n\n"
        f"Provide a concise, clear, 5-sentence explanation of '{query}'."
    )

    print("🧠 Summarizing JSON resources...")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You summarize educational resources concisely and clearly."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=MAX_OUTPUT_TOKENS
    )

    return response.choices[0].message.content.strip()

def main():
    json_data = load_json('resources.json')
    query = input("Enter your search query: ")
    summary = summarize_resources(json_data, query)
    print("\nGenerated Summary:")
    print(summary)

if __name__ == "__main__":
    main()
