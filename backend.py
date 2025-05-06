from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import tldextract
import re
import socket
import requests
import whois

app = Flask(__name__)

# Load model and scaler
model = joblib.load("models_deep/best_xgb_model.pkl")
scaler = joblib.load("models/scaler.pkl")  # If used

def is_private_ip(ip):
    try:
        parts = list(map(int, ip.split('.')))
        return (
            (parts[0] == 10) or
            (parts[0] == 172 and 16 <= parts[1] <= 31) or
            (parts[0] == 192 and parts[1] == 168)
        )
    except:
        return False

def extract_features(url):
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    domain = tldextract.extract(url).registered_domain or ""

    length_url = len(url)
    count_dots = url.count('.')
    count_hyphen = url.count('-')
    count_at = url.count('@')
    count_suspicious = sum(1 for word in ['login', 'signin', 'bank', 'update', 'free', 'lucky'] if word in url.lower())
    has_https = int(parsed.scheme == 'https')

    try:
        ip = socket.gethostbyname(hostname)
        using_ip = int(bool(re.match(r'\d+\.\d+\.\d+\.\d+', hostname)))
        private_ip = int(is_private_ip(ip) or hostname == 'localhost')
    except:
        using_ip = 0
        private_ip = 0

    dns_failed = 0
    try:
        socket.gethostbyname(hostname)
    except:
        dns_failed = 1

    try:
        w = whois.whois(domain)
        whois_available = int(w.domain_name is not None)
    except:
        whois_available = 0

    try:
        rank = int(requests.get(f"https://data.alexa.com/data?cli=10&url={domain}").text.count("<POPULARITY"))
    except:
        rank = 0

    return [
        length_url, count_dots, count_hyphen, count_at, count_suspicious,
        has_https, using_ip, private_ip, dns_failed, whois_available, rank
    ]

@app.route("/detect", methods=["POST"])
def detect():
    try:
        url = request.json.get("url")
        if not url:
            return jsonify({"error": "URL not provided"})

        features = extract_features(url)
        feature_names = [
            'length_url', 'count_dots', 'count_hyphen', 'count_at', 'count_suspicious',
            'has_https', 'using_ip', 'private_ip', 'dns_failed', 'whois_available', 'rank'
        ]

        input_df = pd.DataFrame([features], columns=feature_names)
        input_scaled = scaler.transform(input_df)
        proba = model.predict_proba(input_scaled)[0]
        label = model.predict(input_scaled)[0]
        confidence = float(np.max(proba))

        return jsonify({
            "label": str(label),
            "confidence": confidence
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)