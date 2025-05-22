from flask import Flask, render_template_string, request
import joblib
from datetime import datetime

app = Flask(__name__)

# Load model and vectorizer once
model = joblib.load('D:/project/url/model.pkl')
vectorizer = joblib.load('D:/project/url/vectorizer.pkl')

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>URL Safety Checker</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f4f6fa; margin: 0; padding: 0; }
    .container { max-width: 500px; margin: 60px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px #ccc; padding: 30px; }
    h2 { color: #2c3e50; text-align: center; }
    form { display: flex; flex-direction: column; gap: 15px; }
    input[type="text"] { padding: 10px; font-size: 1.1em; border: 1px solid #ccc; border-radius: 5px; }
    input[type="submit"] { background: #3498db; color: #fff; border: none; padding: 12px; border-radius: 5px; font-size: 1.1em; cursor: pointer; transition: background 0.2s; }
    input[type="submit"]:hover { background: #217dbb; }
    .result-safe { color: #27ae60; font-size: 1.2em; text-align: center; margin-top: 20px; }
    .result-malicious { color: #c0392b; font-size: 1.2em; text-align: center; margin-top: 20px; }
    .footer { text-align: center; color: #888; margin-top: 40px; font-size: 0.97em; }
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
    if request.method == 'POST':
        url = request.form['url']
        url_vec = vectorizer.transform([url])
        prediction = model.predict(url_vec)[0]
        if prediction == 'benign':
            result = "✔ The website is SAFE ✅"
            result_class = "result-safe"
        else:
            result = "❌ The website is MALICIOUS 🚫"
            result_class = "result-malicious"
    return render_template_string(HTML, result=result, result_class=result_class)

if __name__ == '__main__':
    app.run(debug=True)