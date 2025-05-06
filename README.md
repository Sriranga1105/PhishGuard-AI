# PhishGuard-AI 🛡️  
Phishing Detection using Machine Learning and Browser Extension

PhishGuard-AI is a real-time phishing detection system that combines a browser extension frontend with a Flask-based machine learning backend. The system analyzes website URLs and their associated features to detect potential phishing attacks and warn users instantly.

---

## 🔍 Features

- ✅ Real-time phishing detection
- 🧠 Trained XGBoost model with 85%+ accuracy and 0.91 AUC
- 📊 Feature engineering with WHOIS, DNS, and HTML analysis
- 📈 Threshold tuning and uncertainty estimation
- 🧪 SMOTE-based class balancing
- 🌐 Browser extension for user interaction
- 📡 Backend server powered by Flask
- ✉️ Alerts and detailed risk prediction

---

## 📁 Project Structure

![Screenshot_20250506_214950](https://github.com/user-attachments/assets/1ccb5fd6-55e4-4232-9aed-ae62991b4688)

---

## ⚙️ Installation & Usage

### 🔧 Backend Setup (Flask + ML Model)

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/PhishGuard-AI.git
   cd PhishGuard-AI/backend
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```bash
   python app.py
   ```
   The Flask server will run at http://localhost:5000/ and accept requests from the browser extension.
---
## 🌐 Frontend (Browser Extension)
    Open Chrome and go to: chrome://extensions/

    Enable Developer mode.

    Click "Load unpacked" and select the extension/ folder.

    Use the popup to test any URL. It sends the data to the backend and displays predictions.
---
## 🤖 Machine Learning Model

    Model: XGBoost Classifier

    Training Features:

        URL-based features

        WHOIS data (domain age, registrar)

        DNS lookup (IP, resolution time)

        HTML/JS keyword patterns

    Preprocessing:

        SMOTE for class balancing

        Feature scaling (StandardScaler)

        Feature selection using importance scores

    Threshold: Tuned to 0.4 for improved recall
---
## 📊 Dataset Summary
* ✅ 5,000 legitimate URLs (legitimate.csv)

* ⚠️ 5,000 phishing URLs (phishing.csv)
* 📈 Combined dataset: urldata.csv (10,000 entries)

Source: PhishTank, UNB dataset
---
## 📦 Dependencies

* Python 3.8+
* Flask
* Scikit-learn
* XGBoost
* Pandas
* NumPy
* requests
* tldextract
* python-whois
---
## 📸 Screenshots
![image](https://github.com/user-attachments/assets/aee28b1b-d892-45de-94bd-88d812a6d69c)

![image](https://github.com/user-attachments/assets/79992d6f-28f1-44f8-948f-a04036196ceb)

![image](https://github.com/user-attachments/assets/41ae8c25-c01e-4590-b030-32a63833e4dc)

---
## 🔐 Security Considerations

* Only tested on localhost; production deployment requires HTTPS and secure API handling.
* Avoid sharing private model files publicly (e.g., .pkl files without proper licensing or obfuscation).
---
## 🙌 Acknowledgements

    PhishTank for phishing URL dataset

    UNB for legitimate website data

    Stack Overflow & OpenAI for guidance
---
### 📄 License

MIT License

Copyright (c) 2025 Sriranganathan M

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



