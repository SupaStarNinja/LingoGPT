from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai

app = Flask(__name__)
cors = CORS(app, origins='*')

# Initialize the Gemini API client
client = genai.Client(api_key='AIzaSyAUHjaH0PsHO3vjR2h-dRaghilt2LVdpDE')

@app.route("/api/users", methods=['GET'])
def users():
    return jsonify(
        {
            "users": ["Khatib", "Mehdick", "Piano"]
        }
    )

@app.route("/api/yoda-chat", methods=['POST'])
def yoda_chat():
    # Get the user input from the request
    data = request.get_json()
    user_question = data.get('text', '')
    
    # Process the input with Gemini API
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"Convert this text to Yoda's speech pattern: {user_question}"
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)