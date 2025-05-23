import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY3")  
genai.configure(api_key=GEMINI_API_KEY)

def get_short_tips(query):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Give short tips or a concise tutorial for: {query}")
    
    if response:
        # Limit to 450 words
        words = response.text.split()[:450]  
        limited_response = ' '.join(words)
        return limited_response
    else:
        return "Sorry, I couldn't generate tips or tutorials."

@app.route("/predict", methods=["GET"])
def predict():
    query = request.args.get("q", "").strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    tips = get_short_tips(query)
    return jsonify({"tips": tips})

if __name__ == "__main__":
    app.run(debug=True)
