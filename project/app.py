import pandas as pd
import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse
import re

# Load the dataset
dataset = pd.read_csv(r"C:\Users\Sarthak Garg\Dataset.csv")
if "Domain" in dataset.columns:
    dataset.set_index("Domain", inplace=True)
    print("Dataset index set to 'Domain'")
else:
    raise ValueError("The 'Domain' column is missing from the dataset.")

# Load the trained model
with open("XGBoostClassifier.pickle.dat", "rb") as model_file:
    model = pickle.load(model_file)

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Function to extract features from URL
def extract_features(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc or parsed_url.path

    # Feature extraction logic
    features = [
        int(bool(re.match(r'\d+\.\d+\.\d+\.\d+', domain))),  # Have_IP: checks if the domain contains an IP address (e.g., 192.168.1.1)
        int('@' in url),  # Have_At: checks if the URL contains '@'
        int(len(url) > 0),  # URL_Length: checks if URL is non-empty, assigns 1 for any URL length
        int(url.count('/') > 1),  # URL_Depth: checks if the URL contains more than one '/'
        int('//' in url),  # Redirection: checks if the URL contains '//' indicating redirection
        int('https' in url),  # https_Domain: checks if the URL uses 'https'
        int(len(url) < 20),  # TinyURL: checks if the URL length is less than 20 characters
        int('-' in url),  # Prefix/Suffix: checks if the URL contains '-'
        int(domain in dataset.index),  # DNS_Record: checks if the domain exists in the dataset
        int(bool(re.search(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', url))),  # Web_Traffic: checks if the URL contains an IP address pattern (rudimentary check for traffic indicators)
        int(len(domain) > 5),  # Domain_Age: checks if the domain has more than 5 characters (a proxy for domain age)
        int(domain.endswith('.com')),  # Domain_End: checks if the domain ends with '.com' (arbitrary choice)
        int('<iframe' in url),  # iFrame: checks if the URL contains an iframe
        int('mouseover' in url),  # Mouse_Over: checks if 'mouseover' appears in the URL (rudimentary check)
        int('contextmenu' in url),  # Right_Click: checks if 'contextmenu' appears in the URL (rudimentary check)
        int('forward' in url)  # Web_Forwards: checks if 'forward' appears in the URL (rudimentary check)
    ]
    
    return features

# Helper function to extract the domain part of a URL
def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc or parsed_url.path

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get("url")
    print("Received URL for prediction:", url)

    # Extract the domain from the URL
    domain = get_domain(url)
    print("Processed domain for lookup:", domain)

    # Check if the domain is in the dataset
    if domain in dataset.index:
        label = dataset.loc[domain, "Label"]
        
        # If there are multiple entries for the same domain, take the first one
        if isinstance(label, pd.Series):
            label = label.iloc[0]
        
        result = "phishing" if label == 1 else "legitimate"
        print(f"URL found in dataset, label: {result}")
        probability = 1.0 if label == 1 else 0.0  # certainty based on dataset
    else:
        # Domain not in dataset, so use the model to predict
        features = extract_features(url)
        probability = float(model.predict_proba([features])[0][1])  # Convert to Python float
        result = "phishing" if probability <= 0.5 else "legitimate"
        print("Using model prediction:", result , probability)

    return jsonify({"prediction": result, "probability": probability})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
