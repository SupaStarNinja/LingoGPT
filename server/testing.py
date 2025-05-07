import json
import os
from bert_score import score
from flask_cors import CORS
from yoda import Yoda

import requests



def load_training_data():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')

    # Load JSON training pairs
    with open(os.path.join(data_dir, 'testing_pairs.json'), 'r') as f:
        training_pairs = json.load(f)['examples']

    return training_pairs

def main():
    yoda = Yoda()
    training = load_training_data()

    for text in training:
        human = text['input']
        predicted = yoda.translate(human)
        print("response: " + predicted)
        text['predicted'] = predicted

    yoda_texts = [text['output'] for text in training]
    pred_yoda_texts = [text['predicted'] for text in training]

    # Compute BERTScore for the predicted Yoda translations against the ground truth.
    P, R, F1 = score(pred_yoda_texts, yoda_texts, lang="en", verbose=True)

    # Print average BERTScore metrics.
    print(f"BERTScore Precision: {P.mean():.4f}")
    print(f"BERTScore Recall: {R.mean():.4f}")
    print(f"BERTScore F1: {F1.mean():.4f}")
    print("")

    # Print individual samples along with their BERTScore F1 values.
    for i, text in enumerate(training):
        human = text['input']
        yoda = text['output']
        pred_yoda = text['predicted']
        print("Human: " + human)
        print("Yoda: " + yoda)
        print("Pred_Yoda: " + pred_yoda)
        print(f"BERT F1 Score for this sample: {F1[i]:.4f}")
        print("")

if __name__ == "__main__":
    main()