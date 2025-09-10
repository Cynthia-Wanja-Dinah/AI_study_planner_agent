# backend/app.py
import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Configure Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=gemini_api_key)

# Initialize Flask
app = Flask(__name__, template_folder='../templates')

# Function to generate a response using Gemini
def generate_response(user_message: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")  # You can change model if needed
    response = model.generate_content(user_message)
    return response.text if response and response.text else "⚠️ No response from model."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    payload = request.get_json(silent=True) or {}
    user_message = payload.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response_text = generate_response(user_message)
        return jsonify({'response': response_text})
    except Exception as e:
        app.logger.error(f"Error generating response: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render sets $PORT
    app.run(host="0.0.0.0", port=port, debug=True)
