import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Get the absolute path for the templates folder
# This is a more robust way to handle the templates path
templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))
app = Flask(__name__, template_folder=templates_dir)

# Configure Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    # A cleaner way to handle missing API key in a web application
    print("❌ GEMINI_API_KEY not found in environment variables. The API will not be functional.")
else:
    genai.configure(api_key=gemini_api_key)

# Function to generate a response using Gemini
def generate_response(user_message: str) -> str:
    """Generates a response from the Gemini API."""
    if not gemini_api_key:
        return "⚠️ API key is not configured. Please set GEMINI_API_KEY."
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_message)
        return response.text if response and response.text else "⚠️ No response from model."
    except Exception as e:
        app.logger.error(f"Error generating response from Gemini API: {e}", exc_info=True)
        return f"⚠️ An error occurred: {str(e)}"

@app.route('/')
def index():
    """Serves the main chat application page."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handles chat messages and returns a response from the Gemini API."""
    payload = request.get_json(silent=True) or {}
    user_message = payload.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    response_text = generate_response(user_message)
    return jsonify({'response': response_text})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
