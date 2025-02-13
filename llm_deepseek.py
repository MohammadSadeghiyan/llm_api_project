from flask import Flask, request, jsonify
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


API_URL = "https://api.metisai.ir/api/v1/wrapper/deepseek/chat/completions"
API_KEY = os.getenv("secret_key")

@app.route('/generate', methods=['POST'])
def generate_text():
    user_input = request.json.get("text", "")
    
    if not user_input:
        return jsonify({"error": "No text provided"}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 150
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0:
            generated_text = response_data["choices"][0]["message"]["content"].strip()

          
            return app.response_class(
                response=json.dumps({"generated_text": generated_text}, ensure_ascii=False),
                status=200,
                mimetype='application/json; charset=utf-8'
            )
        else:
            return jsonify({"error": "Invalid response from DeepSeek API"}), 500

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
