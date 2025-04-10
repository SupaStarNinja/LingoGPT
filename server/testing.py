import json
import os
from bert_score import score

import requests


url = "http://localhost:8080/api/yoda-chat"

def get_response(message):
    # Prepare the payload with the provided message.
    payload = {"text": message}

    try:
        # Send a POST request with the JSON payload to the API.
        response = requests.post(url, json=payload)

        # Raise an HTTPError if the response status code indicates an error.
        response.raise_for_status()

        # Parse the JSON response.
        json_response = response.json()

        # Return the 'response' field if it exists.
        return json_response.get("response", "No response provided.")

    except requests.HTTPError as http_err:
        error_message = f"HTTP error occurred: {http_err}"
        print(error_message)
        return error_message
    except Exception as err:
        error_message = f"Other error occurred: {err}"
        print(error_message)
        return error_message

def load_training_data():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')

    # Load JSON training pairs
    with open(os.path.join(data_dir, 'testing_pairs.json'), 'r') as f:
        training_pairs = json.load(f)['examples']

    return training_pairs

def main():

    training = load_training_data()

    for text in training:
        human = text['input']
        predicted = get_response(human)
        print("response: " + predicted)
        text['predicted'] = predicted

    yoda_texts = [text['truth'] for text in training]
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
        yoda = text['truth']
        pred_yoda = text['predicted']
        print("Human: " + human)
        print("Yoda: " + yoda)
        print("Pred_Yoda: " + pred_yoda)
        print(f"BERT F1 Score for this sample: {F1[i]:.4f}")
        print("")

if __name__ == "__main__":
    main()