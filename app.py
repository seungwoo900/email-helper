from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os, re, json, requests

load_dotenv()  # Load environment variables from .env file

# HF_API_TOKEN = os.getenv('HF_API_TOKEN')

# client = InferenceClient(
#     provider='featherless-ai',
#     api_key=HF_API_TOKEN,
# )

PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
PERPLEXITY_ENDPOINT = "https://api.perplexity.ai/chat/completions"

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
        Read the entire email below and return ONLY valid JSON with this exact structure, 
        in the same sentence order unless you recommend a different logical flow:

        {{
        "paragraphs": [
            {{
            "sentences": [
                {{
                "original": "<the original sentence>",
                "corrected": <null or "<grammar-corrected sentence>">,
                "simplified": <null or "<simplified sentence>">,
                "reason": <null or "<modification reason, up to 7 words>">
                }},
                …
            ]
            }},
            …
        ]
        }}

        Rules:
        1. You may reorder or delete sentences to improve overall flow.
        2. **If you delete a sentence**, still include it with:
        - `"corrected": null`
        - `"simplified": null`
        - a non-null `"reason"` explaining **why** it was removed (e.g. “redundant”).
        3. If you modify for grammar:
        - put the fixed sentence in `"corrected"`,
        - `"simplified": null`,
        - `"reason"` a detailed note up to 7 words (e.g. “grammar error”).
        4. If you simplify for clarity or tone:
        - `"corrected": null`,
        - put the simpler version in `"simplified"`,
        - `"reason"` a detailed note up to 7 words (e.g. “too formal”).
        5. If already correct & concise:
        - set `"corrected"`, `"simplified"`, `"reason"` all to null.
        6. Remove all newline (“\\n”) and backslash (“\\”) characters from every field.
        7. Output **only** the JSON—no extra text.

        Email content:
        \"\"\"\n{full_text}\n\"\"\"
        """

    # Call Perplexity API
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "sonar",       # Choose Perplexity model
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    resp = requests.post(PERPLEXITY_ENDPOINT, json=body, headers=headers)

    if not resp.ok:
        return jsonify({"error": "Perplexity API error", "details": resp.text}), 500

    # extract the AI’s reply
    raw_resp = resp.json()["choices"][0]["message"]["content"].strip()

        # ——— strip markdown fences if present ———
    if raw_resp.startswith("```"):
        parts = raw_resp.split("```")
        # parts might be ['', 'json\n{...}', '']
        middle = parts[1] if len(parts) > 2 else parts[0]
        lines = middle.splitlines()
        # drop a leading "json" label line if any
        if lines and lines[0].strip().lower().startswith("json"):
            lines = lines[1:]
        raw_resp = "\n".join(lines).strip()

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