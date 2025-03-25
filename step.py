import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY3")  # Set this in your Vercel environment variables
genai.configure(api_key=GEMINI_API_KEY)

# Define the function to get step-by-step instructions
def get_instructions(query):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"Give step-by-step instructions for: {query}")
    return response.text if response else "Sorry, I couldn't generate instructions."

@app.route("/predict", methods=["GET"])
def predict():
    query = request.args.get("q", "").strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    instructions = get_instructions(query)
    return jsonify({"instructions": instructions})

# Run Flask app (for local testing)
if __name__ == "__main__":
    app.run(debug=True)