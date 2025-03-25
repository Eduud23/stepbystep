import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY3")  
genai.configure(api_key=GEMINI_API_KEY)

def get_short_tips(query):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"Give short tips or a concise tutorial for: {query}")
    tips = response.text if response else "Sorry, I couldn't generate tips or tutorials."
    
    # Add the "Important" note at the end of the response
    important_note = "**Important:** If you're uncomfortable or unsure about any step, call or go for local services.  Don't risk injury."
    
    return f"{tips}\n\n{important_note}"

@app.route("/predict", methods=["GET"])
def predict():
    query = request.args.get("q", "").strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    tips = get_short_tips(query)
    return jsonify({"tips": tips})

if __name__ == "__main__":
    app.run(debug=True)
