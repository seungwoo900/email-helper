from flask import Flask, request, jsonify
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os, re, json

load_dotenv()  # Load environment variables from .env file
HF_API_TOKEN = os.getenv('HF_API_TOKEN')

client = InferenceClient(
    provider='featherless-ai',
    api_key=HF_API_TOKEN,
)

app = Flask(__name__)

def split_sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json() 
    raw = data.get('text', '')
    try:
        full_text = json.loads(raw)
    except:
        full_text = raw

    # Prompt for the model
    prompt = f"""
        You are a professional English-writing assistant for non-native speakers.
        Read the entire email below and return ONLY valid JSON with this exact structure:

        {{
        "paragraphs": [
            {{
            "sentences": [
                {{
                "original": "<the original sentence>",
                "corrected": <null or "<grammar-corrected sentence>">,
                "simplified": <null or "<simplified sentence>">
                }},
                …
            ]
            }},
            …
        ]
        }}

        Rules for each sentence:
        1. If the sentence contains any grammatical errors, put the fully corrected sentence in "corrected" and set "simplified" to null.
        2. If there are no grammatical errors but the sentence is overly formal, stiff, or complex, set "corrected" to null and put the simpler version in "simplified."
        3. If there are no grammatical errors and the sentence is already simple enough, set both "corrected" and "simplified" to null.

        Email content:
        \"\"\"\n{full_text}\n\"\"\"

        Output only the JSON. Do not include any explanations, notes, or additional text.
    """

    # Call the model once
    completion = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[{"role":"user","content":prompt}],
    )
    raw_resp = completion.choices[0].message.content.strip()

    # JSON Parsing
    try:
        result = json.loads(raw_resp)
    except json.JSONDecodeError:
        app.logger.error("Failed to parse /analyze response:\n%s", raw_resp)
        return jsonify({
            "error": "Invalid JSON from model",
            "raw": raw_resp
        }), 500

    # Validate structure
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)