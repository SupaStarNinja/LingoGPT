from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cors = CORS(app, origins='*')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_training_data():
    try:
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        
        # Load JSON training pairs
        with open(os.path.join(data_dir, 'training_pairs.json'), 'r') as f:
            training_pairs = json.load(f)['examples']
        
        # Load wisdom quotes
        with open(os.path.join(data_dir, 'wisdom_quotes.txt'), 'r') as f:
            wisdom_quotes = f.read().strip()
        
        # Load battle dialogue
        with open(os.path.join(data_dir, 'battle_dialogue.txt'), 'r') as f:
            battle_dialogue = f.read().strip()
        
        return training_pairs, wisdom_quotes, battle_dialogue
    except Exception as e:
        print(f"Error loading training data: {str(e)}")
        return [], "", ""  # Return empty data if files can't be loaded

def create_yoda_prompt(user_text):
    training_pairs, wisdom_quotes, battle_dialogue = load_training_data()
    
    # Create prompt with examples from different sources
    prompt = "Convert the following text to sound like Yoda from Star Wars. Here are some examples:\n\n"
    
    # Add training pairs if available
    if training_pairs:
        for pair in training_pairs[:3]:  # Use first 3 examples
            prompt += f"Original: {pair['input']}\n"
            prompt += f"Yoda: {pair['output']}\n\n"
    
    # Add wisdom quotes if available
    if wisdom_quotes:
        prompt += "Some of Yoda's wisdom:\n"
        prompt += wisdom_quotes.split('\n\n')[0] + '\n\n'  # Add first wisdom quote
    
    # Add battle dialogue if available
    if battle_dialogue:
        prompt += "Some of Yoda's battle dialogue:\n"
        prompt += battle_dialogue.split('\n\n')[0] + '\n\n'  # Add first battle quote
    
    # Add the user's text
    prompt += f"Now convert this text to Yoda's speech pattern:\n"
    prompt += f"Text: {user_text}\n\n"
    prompt += "Yoda's speech:"
    
    return prompt

@app.route("/api/users", methods=['GET'])
def users():
    return jsonify(
        {
            "users": ["Khatib", "Mehdick", "Piano", "Ruthusford"]
        }
    )

@app.route("/api/yoda-chat", methods=['POST'])
def yoda_chat():
    try:
        data = request.get_json()
        user_question = data.get('text', '')
        
        if not user_question:
            return jsonify({"error": "No text provided"}), 400
            
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({"error": "OpenAI API key not configured"}), 500
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Master Yoda from Star Wars. You help convert normal English text into Yoda's unique speech pattern."},
                {"role": "user", "content": create_yoda_prompt(user_question)}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        print(f"Error in yoda_chat: {str(e)}")  # Log the error
        return jsonify({"error": "Failed to process request. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)