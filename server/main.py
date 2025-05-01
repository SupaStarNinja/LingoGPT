import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from flask import Flask, request, jsonify
import json
import random
import os

data_dir = os.path.join(os.path.dirname(__file__), 'data')
 
# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load training pairs
with open(os.path.join(data_dir, 'training_pairs.json'), 'r') as f:    
    data = json.load(f)
pairs = data["examples"]

# --- RULE-BASED REWRITER ---
def yoda_rewrite_rule(sentence):
    doc = nlp(sentence)
    subject = None
    root = None
    objects = []

    for token in doc:
        if token.dep_ == "nsubj":
            subject = token
        elif token.dep_ == "ROOT":
            root = token
        elif "obj" in token.dep_:
            objects.append(token)

    # Reconstruct Yoda sentence: [object] [subject] [verb]...
    front = " ".join([chunk.text for chunk in objects]) if objects else ""
    subj = subject.text if subject else ""
    verb = root.text if root else ""
    
    remainder = " ".join([t.text for t in doc if t not in [subject, root] + objects])
    
    return f"{front}, {subj} {verb} {remainder}".strip().replace("  ", " ")

# --- BUILD DATASET FOR CLASSIFIER ---
X = []
y = []

for ex in pairs:
    input_sentence = ex["input"]
    expected_yoda = ex["output"]
    rewritten = yoda_rewrite_rule(input_sentence)
    
    # Label 1 = good match, 0 = bad match (rough heuristic)
    is_match = expected_yoda.lower().split()[0] in rewritten.lower().split()
    
    X.append(rewritten)
    y.append(int(is_match))

# Vectorize + train classifier
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)
clf = LogisticRegression()
clf.fit(X_vec, y)

# --- API for live testing ---
app = Flask(__name__)

@app.route("/api/yoda-chat", methods=["POST"])
def to_yoda():
    sentence = request.json["sentence"]
    rule_output = yoda_rewrite_rule(sentence)
    prediction = clf.predict(vectorizer.transform([rule_output]))[0]

    if prediction:
        result = rule_output
    else:
        # fallback (you could use nearest example here)
        result = "Fallback: " + rule_output

    return jsonify({"yoda": result})

if __name__ == "__main__":
    app.run(debug=True)