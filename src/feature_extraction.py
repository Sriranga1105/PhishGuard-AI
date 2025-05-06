import pandas as pd
import re
from urllib.parse import urlparse

def has_ip_address(url):
    """Check if the URL contains an IP address."""
    pattern = r'(([0-9]{1,3}\.){3}[0-9]{1,3})'
    return 1 if re.search(pattern, url) else 0

def count_dots(url):
    """Count number of dots in the URL."""
    return url.count('.')

def count_hyphens(url):
    """Count number of hyphens in the URL."""
    return url.count('-')

def count_at_symbols(url):
    """Count @ symbols in the URL."""
    return url.count('@')

def is_https(url):
    """Check if the URL uses HTTPS."""
    return 1 if urlparse(url).scheme == 'https' else 0

def url_length(url):
    """Return length of the URL."""
    return len(url)

def count_subdomains(url):
    """Count subdomains (e.g., sub1.sub2.example.com = 2)"""
    return len(urlparse(url).netloc.split('.')) - 2

def suspicious_words(url):
    """Check for phishing-related keywords."""
    words = ['login', 'secure', 'account', 'update', 'verify', 'bank', 'signin']
    return sum(word in url.lower() for word in words)

def extract_features(df):
    """Apply all feature functions to a DataFrame with a 'url' column."""
    df['url_length'] = df['url'].apply(url_length)
    df['has_ip'] = df['url'].apply(has_ip_address)
    df['num_dots'] = df['url'].apply(count_dots)
    df['num_hyphens'] = df['url'].apply(count_hyphens)
    df['num_at'] = df['url'].apply(count_at_symbols)
    df['is_https'] = df['url'].apply(is_https)
    df['num_subdomains'] = df['url'].apply(count_subdomains)
    df['suspicious_words'] = df['url'].apply(suspicious_words)
    return df

def process_and_save(input_path, label, output_path):
    """Load raw URLs, extract features, add label, and save."""
    df = pd.read_csv(input_path, names=["url"])  # assuming only one column
    df = extract_features(df)
    df['label'] = label
    df.to_csv(output_path, index=False)
    print(f"✅ Features extracted and saved to {output_path}")