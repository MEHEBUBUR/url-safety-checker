from flask import Flask, render_template_string, request
import joblib
from datetime import datetime

app = Flask(__name__)

# Load model and vectorizer once
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>URL Safety Checker</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://fonts.googleapis.com/css?family=Inter:400,600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
      background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
      margin: 0;
      padding: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
    .container {
      max-width: 440px;
      width: 96vw;
      margin: 40px auto 0 auto;
      background: #fff;
      border-radius: 20px;
      box-shadow: 0 8px 32px rgba(120, 72, 232, 0.13), 0 2px 8px #b0c4de;
      padding: 38px 32px 28px 32px;
      display: flex;
      flex-direction: column;
      align-items: center;
      border: 2px solid #a8edea;
      transition: box-shadow 0.2s;
    }
    .container:hover {
      box-shadow: 0 12px 36px rgba(120, 72, 232, 0.18), 0 4px 16px #b0c4de;
    }
    h2 {
      color: #7d5fff;
      text-align: center;
      font-weight: 700;
      letter-spacing: 0.5px;
      margin-bottom: 18px;
      font-size: 2.1em;
    }
    form {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 18px;
      margin-bottom: 10px;
    }
    input[type="text"] {
      padding: 15px;
      font-size: 1.1em;
      border: 1.5px solid #7ed6df;
      border-radius: 10px;
      outline: none;
      transition: border 0.2s, box-shadow 0.2s;
      background: #f8fafc;
      box-shadow: 0 1px 3px #e0eafc;
    }
    input[type="text"]:focus {
      border: 1.5px solid #7d5fff;
      background: #f0f8ff;
      box-shadow: 0 2px 8px #b0c4de;
    }
    input[type="submit"] {
      background: linear-gradient(90deg, #7ed6df 60%, #7d5fff 100%);
      color: #fff;
      border: none;
      padding: 16px;
      border-radius: 10px;
      font-size: 1.1em;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
      box-shadow: 0 2px 8px #e3eafc;
      letter-spacing: 0.2px;
    }
    input[type="submit"]:hover {
      background: linear-gradient(90deg, #7d5fff 60%, #7ed6df 100%);
      box-shadow: 0 4px 16px #b0c4de;
      transform: translateY(-2px) scale(1.03);
    }
    .result-safe, .result-malicious {
      font-size: 1.18em;
      text-align: center;
      margin-top: 22px;
      padding: 13px 0;
      border-radius: 10px;
      font-weight: 600;
      letter-spacing: 0.2px;
      width: 100%;
      box-sizing: border-box;
    }
    .result-safe {
      color: #20bf6b;
      background: #eafaf1;
      border: 1.5px solid #7ed6df;
    }
    .result-malicious {
      color: #eb2f06;
      background: #fff0f3;
      border: 1.5px solid #f5b7b1;
    }
    .reason {
      font-size: 1em;
      color: #555;
      margin-top: 10px;
      text-align: center;
      background: #f8fafc;
      border-radius: 9px;
      padding: 12px 14px;
      border: 1px solid #e0eafc;
      box-shadow: 0 1px 3px #e3eafc;
      width: 100%;
      box-sizing: border-box;
    }
    .footer {
      text-align: center;
      color: #888;
      margin-top: 38px;
      font-size: 0.98em;
      letter-spacing: 0.1px;
    }
    @media (max-width: 600px) {
      body {
        align-items: flex-start;
        justify-content: flex-start;
      }
      .container {
        max-width: 99vw;
        padding: 18px 4vw 18px 4vw;
        margin: 10px auto;
        border-radius: 12px;
      }
      h2 {
        font-size: 1.3em;
      }
      input[type="text"], input[type="submit"] {
        font-size: 1em;
        padding: 13px;
      }
      .reason {
        font-size: 0.98em;
        padding: 10px 6px;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>🔎 URL Safety Checker</h2>
    <form method="post">
      <input type="text" name="url" size="60" placeholder="Paste URL here (e.g. https://example.com)" required>
      <input type="submit" value="Check URL">
    </form>
    {% if result is not none %}
      <div class="{{ result_class }}">{{ result }}</div>
      {% if reason %}
        <div class="reason">{{ reason }}</div>
      {% endif %}
    {% endif %}
  </div>
  <div class="footer">
    <span>
      This application was developed by <b>Mehebubur Rahman</b> and <b>Rudradev Chaudhury</b> as part of a school project.<br>
      All rights reserved.
    </span>
  </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    result_class = ""
    reason = ""
    if request.method == 'POST':
        url = request.form['url']
        url_vec = vectorizer.transform([url])
        prediction = model.predict(url_vec)[0]
        if prediction == 'benign':
            result = "✔ The website is SAFE ✅"
            result_class = "result-safe"
            reason = "This link appears safe because it matches patterns of legitimate websites and does not contain suspicious features."
        else:
            result = "❌ The website is MALICIOUS 🚫"
            result_class = "result-malicious"
            reason = "This link is flagged as malicious because it matches patterns commonly found in phishing or harmful sites."
    return render_template_string(HTML, result=result, result_class=result_class, reason=reason)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)