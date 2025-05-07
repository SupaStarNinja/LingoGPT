import spacy
from flask import Flask, request, jsonify
from flask_cors import CORS
from yoda import Yoda


yoda = Yoda()


# --- API for live testing ---
app = Flask(__name__)
CORS(app)


@app.route("/api/yoda-chat", methods=["POST"])
def to_yoda():
    sentence = request.json["text"]

    result = yoda.translate(sentence)

    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)