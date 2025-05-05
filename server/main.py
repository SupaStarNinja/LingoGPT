import spacy
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import os

data_dir = os.path.join(os.path.dirname(__file__), 'data')

# Load spaCy model
parser = spacy.load("en_core_web_sm")
model_save_path = os.path.join(os.path.dirname(__file__), 'models', 'rearrangement_model')
print("Path to yoda model:" + model_save_path)
model = T5ForConditionalGeneration.from_pretrained(model_save_path)
tokenizer = T5Tokenizer.from_pretrained(model_save_path)

# --- API for live testing ---
app = Flask(__name__)
CORS(app)

def prepare_input(parser, input):
    prepared_input = ""
    doc = parser(input.strip())

    for token in doc:
        prepared_input += str(token) + "|" + str(token.dep_) + " "

    return prepared_input


def translate_prepared_input(tokenizer, model, prepared_input):
    inputs = tokenizer(prepared_input, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=64)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


@app.route("/api/yoda-chat", methods=["POST"])
def to_yoda():
    sentence = request.json["text"]

    test_input = prepare_input(parser, sentence)

    result = translate_prepared_input(tokenizer, model, test_input)

    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)