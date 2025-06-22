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
    """
    Analyze a sentence for difficulty and tone using Hugging Face Inference API.
    Example input: { "sentence": "The quick brown fox jumps over the lazy dog." }
    Example response: { "difficulty": "easy", "tone": "friendly" }
    """

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

@app.route('/rewrite', methods=['POST'])
def rewrite():
    """
    Rewrite a sentence to be simpler and more friendly.
    Example input: { "sentence": "Can you also tell me how much utilities per month will be?" }
    Example response:
    {
        "original": "Can you also tell me how much utilities per month will be?",
        "rewritten_sentence": "Could you please estimate my monthly utility bills for me?"
    }
    """
    data = request.get_json()
    sentence = data.get('sentence', '')
    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400
    
    prompt = (
        f"Rewrite the following sentence to be simpler and more friendly:\n"
        f"Sentence: \"{sentence}\"\n"
        f"Output only the rewritten sentence."
    )

    try:
        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        rewritten_sentence = completion.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({
        "original": sentence,
        "rewritten_sentence": rewritten_sentence
        })

if __name__ == '__main__':
    app.run(debug=True)