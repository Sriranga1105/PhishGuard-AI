# backend.py (Flask API Server)
from flask import Flask, jsonify, request
from flask_cors import CORS
from urllib.parse import urlparse
import tldextract
import whois
import socket
import re
import requests
import joblib
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app)

# Load model and scaler
model = joblib.load('xgb_model.pkl')
scaler = joblib.load('scaler.pkl')

FEATURE_ORDER = [
    'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
    'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record',
    'Web_Traffic', 'Domain_Age', 'Domain_End', 'iFrame',
    'Mouse_Over', 'Right_Click', 'Web_Forwards'
]

executor = ThreadPoolExecutor(max_workers=4)

def is_ip_address(domain):
    try:
        socket.inet_aton(domain)
        return 1
    except:
        return 0

def get_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc.split(':')[0]
    features = {
        'Have_IP': is_ip_address(domain),
        'Have_At': 1 if '@' in url else 0,
        'URL_Length': len(url),
        'URL_Depth': url.count('/'),
        'Redirection': 1 if '//' in url[8:] else 0,
        'https_Domain': 0 if parsed.scheme == 'https' else 1,
        'TinyURL': 1 if any(x in url for x in ['tinyurl', 'bit.ly']) else 0,
        'Prefix/Suffix': 1 if '-' in tldextract.extract(url).domain else 0,
        'DNS_Record': 0,
        'Web_Traffic': 0,
        'Domain_Age': 0,
        'Domain_End': 0,
        'iFrame': 0,
        'Mouse_Over': 0,
        'Right_Click': 0,
        'Web_Forwards': 0
    }

    try:
        info = whois.whois(domain)
        creation_date = info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        features['Domain_Age'] = (datetime.now() - creation_date).days if creation_date else 0
        features['DNS_Record'] = 1 if info.domain_name else 0
    except:
        pass

    return [features[key] for key in FEATURE_ORDER]

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url', '')
    
    features = get_features(url)
    scaled = scaler.transform([features])
    prob = model.predict_proba(scaled)[0][1]
    
    return jsonify({
        'url': url,
        'phishing': bool(prob > 0.5),
        'confidence': float(prob),
        'features': dict(zip(FEATURE_ORDER, features))
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, threaded=True)