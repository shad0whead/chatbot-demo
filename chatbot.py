from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Get xAI API key from environment variable (set on Render) or use a default (for local testing)
xai_api_key = os.environ.get('XAI_API_KEY', 'Bearer xai-CJp6tguM7MX5W1d3HGNgg5fCqJih7GAatUZJfoIMrla36KDjZzZL6hcO0iGFV71x8b5w3vdflrGzsPC1')
demo_password = "secret123"  # Keep this for login

# Dynamic system prompt based on store type (no coffee shop references)
def get_system_prompt(store_type):
    today_date = datetime.now().strftime('%B %d, %Y')
    if store_type == "TechTrend Electronics":
        return f"You’re a professional electronics store bot, TechTrend Electronics, offering products like headphones, TVs, phones, and gadgets, hours 9 AM to 9 PM daily. Answer in a professional, friendly tone. Today’s date is {today_date}, but only mention the date if asked directly."
    elif store_type == "AutoGear Online":
        return f"You’re a professional automotive online retailer bot, AutoGear Online, selling tires, car parts, and accessories, hours 9 AM to 9 PM daily. Answer in a professional, friendly tone. Today’s date is {today_date}, but only mention the date if asked directly."
    elif store_type == "StyleHub Clothing":
        return f"You’re a professional clothing store bot, StyleHub Clothing, offering apparel like shirts, dresses, and accessories, hours 9 AM to 9 PM daily. Answer in a professional, friendly tone. Today’s date is {today_date}, but only mention the date if asked directly."
    elif store_type == "HomeHaven Furniture":
        return f"You’re a professional furniture store bot, HomeHaven Furniture, selling couches, tables, chairs, and more, hours 9 AM to 9 PM daily. Answer in a professional, friendly tone. Today’s date is {today_date}, but only mention the date if asked directly."
    else:  # Default for SmartBiz or unrecognized store
        return f"You’re a professional general store bot, SmartBiz, offering various products like electronics, clothing, and furniture, hours 9 AM to 9 PM daily. Answer in a professional, friendly tone. Today’s date is {today_date}, but only mention the date if asked directly."

headers = {
    "Content-Type": "application/json",
    "Authorization": xai_api_key
}

@app.route('/')
def serve_index():
    return send_from_directory('.', 'demo-chatbot.html')

@app.route('/login', methods=['POST'])
def login():
    password = request.json.get('password')
    if password != demo_password:
        return jsonify({"error": "Invalid password"}), 401
    return jsonify({"success": True})

@app.route('/chat', methods=['POST'])
def chat():
    # Check if user is logged in
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f"Bearer {demo_password}":
        return jsonify({"error": "Unauthorized, login required"}), 401

    user_input = request.json.get('message')
    store_type = request.json.get('storeType', 'SmartBiz')  # Default to SmartBiz if not provided
    system_prompt = get_system_prompt(store_type)

    data = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "model": "grok-2-latest",
        "stream": False,
        "temperature": 0
    }
    response = requests.post(xai_api_url, json=data, headers=headers)
    reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)