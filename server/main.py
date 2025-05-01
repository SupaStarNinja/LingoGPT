import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from flask import Flask, request, jsonify
from flask_cors import CORS
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

# --- RULE-BASED REWRITER (Improved) ---
def yoda_rewrite_rule(sentence):
    doc = nlp(sentence.strip().rstrip('.')) # Remove trailing period for easier parsing
    
    root = None
    subject = None
    auxiliaries = []
    objects = [] # Direct objects, objects of prepositions, complements
    prep_phrases = []
    remainder_tokens = []
    moved_tokens = set() # Keep track of tokens already placed

    # --- 1. Identify Key Components ---
    for token in doc:
        # Find the main verb/action
        if token.dep_ == "ROOT":
            root = token
            moved_tokens.add(token)
        # Find the subject
        elif token.dep_ in ("nsubj", "nsubjpass"):
            subject = token
            # Add the whole subject phrase (e.g., "The chosen one")
            moved_tokens.update(list(token.subtree))
        # Find auxiliary verbs
        elif token.dep_ in ("aux", "auxpass"):
            auxiliaries.append(token)
            moved_tokens.add(token)
        # Find objects and complements that often move to the front
        elif token.dep_ in ("dobj", "attr", "acomp", "oprd"): # Direct object, attribute, adjectival complement, object predicate
             # Check if it's part of a prepositional phrase already handled
            if token.head.dep_ != "prep":
                objects.append(token)
                moved_tokens.update(list(token.subtree))
        # Find prepositional phrases (identify by the preposition)
        elif token.dep_ == "prep":
            prep_phrase_tokens = list(token.subtree)
            prep_phrases.append(prep_phrase_tokens)
            moved_tokens.update(prep_phrase_tokens)

    # Identify remaining tokens (those not part of subject, root, aux, moved objects/phrases)
    for token in doc:
        if token not in moved_tokens:
            remainder_tokens.append(token)

    # --- 2. Reconstruct Yoda Sentence ---
    
    # Helper to get text from a list of tokens
    def get_text(tokens):
        return " ".join([t.text for t in tokens])

    # Helper to get text for a subtree starting from a token
    def get_subtree_text(token):
         return " ".join([t.text for t in token.subtree])

    yoda_parts = []

    # Add prepositional phrases first
    for phrase_tokens in prep_phrases:
        yoda_parts.append(get_text(phrase_tokens))

    # Add objects/complements
    for obj_token in objects:
         yoda_parts.append(get_subtree_text(obj_token))

    # Add subject phrase
    if subject:
        yoda_parts.append(get_subtree_text(subject))

    # Add the main verb (ROOT)
    if root:
        yoda_parts.append(root.text)
    
    # Add the remaining tokens (often includes adverbs, particles)
    if remainder_tokens:
         yoda_parts.append(get_text(remainder_tokens))

    # Add auxiliary verbs towards the end
    if auxiliaries:
        yoda_parts.append(get_text(auxiliaries))

    # --- 3. Format the Output ---
    # Join parts with spaces, capitalize first word, add period.
    result = ", ".join(filter(None, yoda_parts)) # Join non-empty parts with comma-space
    if not result:
        return sentence # Return original if reconstruction failed

    result = result[0].upper() + result[1:] + "."
    # Clean up potential double spaces or space-comma issues
    result = result.replace(" ,", ",").replace("  ", " ").replace(" .", ".")
    
    return result

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
CORS(app)

@app.route("/api/yoda-chat", methods=["POST"])
def to_yoda():
    sentence = request.json["text"]
    rule_output = yoda_rewrite_rule(sentence)
    prediction = clf.predict(vectorizer.transform([rule_output]))[0]

    if prediction:
        result = rule_output
    else:
        # fallback (you could use nearest example here)
        result = "Fallback: " + rule_output

    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)