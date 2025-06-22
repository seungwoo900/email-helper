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
    # Regular expression to split sentences based on punctuation
    sentence_endings = r'(?<=[.!?])\s+'
    sentences = re.split(sentence_endings, text.strip())
    return [sentence for sentence in sentences if sentence]

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '') # Get the text from the request, if not present, default to empty string
    sentences = split_sentences(text)
    analyzed_sentences = []

    for s in sentences:
        try:
            analysis = analyze_sentence_with_hf(s)
        except Exception as e:
            print(f"Error analyzing sentence '{s}': {e}")
            analysis = {
                "difficulty": "unknown",
                "tone": "unknown",
                "error": str(e)
            }
        
        analyzed_sentences.append({
            "sentence": s,
            "difficulty": analysis.get("difficulty", "unknown"),
            "tone": analysis.get("tone", "unknown"),
        })

    return jsonify({"sentences": analyzed_sentences})

def analyze_sentence_with_hf(sentence):
    # Function to analyze a sentence using Hugging Face Inference API

    prompt = (
        f"Analyze the following sentence for difficulty and tone.\n"
        f"Return JSON with keys 'difficulty' (easy, medium, hard) and 'tone' (friendly, neutral, formal).\n"
        f"Sentence: \"{sentence}\"\n"
        f"JSON output only."
    )

    completion = client.chat.completions.create(
                    model="mistralai/Mistral-7B-Instruct-v0.2",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                )

    response = completion.choices[0].message.content.strip()

    try:
        analysis = json.loads(response)
    except json.JSONDecodeError:
        analysis = {
            "difficulty": "unknown",
            "tone": "unknown",
            "error": "Invalid JSON response from model"
        }
    return analysis


if __name__ == '__main__':
    app.run(debug=True)