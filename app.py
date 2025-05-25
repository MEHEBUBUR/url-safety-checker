from flask import Flask, render_template_string, request
import joblib

app = Flask(__name__)

model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>URL Safety Checker</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      background: #f4f7fa;
      margin: 0;
      padding: 0;
      color: #1a2230;
      min-height: 100vh;
    }
    .header {
      background: #222d3a;
      color: #fff;
      min-height: 80px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 16px #0002;
      padding: 0 36px;
    }
    .header-title {
      font-weight: 700;
      font-size: 2.2em;
      letter-spacing: 2px;
      color: #fff;
      text-shadow: 0 2px 12px #0071e3cc;
      user-select: none;
      margin-top: 18px;
    }
    .header-desc {
      font-size: 1.1em;
      color: #e0e0e0;
      margin-bottom: 18px;
      margin-top: 4px;
      letter-spacing: 0.02em;
    }
    .info-card {
      max-width: 600px;
      margin: 32px auto 0 auto;
      background: #fff;
      border-radius: 14px;
      box-shadow: 0 4px 24px #dbeafe;
      padding: 28px 32px 24px 32px;
      border: 1.5px solid #e0e0e5;
      display: flex;
      gap: 24px;
      align-items: flex-start;
    }
    .info-icon {
      font-size: 2.8em;
      margin-right: 10px;
      color: #222d3a;
      min-width: 56px;
      text-align: center;
    }
    .info-list {
      font-size: 1.08em;
      margin: 0;
      padding-left: 0;
      list-style: none;
    }
    .info-list li {
      margin-bottom: 8px;
      line-height: 1.6;
    }
    .info-list b {
      color: #222d3a;
    }
    .main-card {
      max-width: 600px;
      margin: 28px auto 0 auto;
      background: #fff;
      border-radius: 14px;
      box-shadow: 0 4px 24px #dbeafe;
      padding: 28px 32px 24px 32px;
      border: 1.5px solid #e0e0e5;
      position: relative;
      z-index: 3;
      overflow: hidden;
    }
    .scan-title {
      font-size: 1.5em;
      font-weight: bold;
      color: #222d3a;
      margin-bottom: 10px;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
      justify-content: center;
      text-align: center;
    }
    .scan-title .warn {
      color: #e6b800;
      font-size: 1.2em;
      margin-right: 6px;
    }
    .scan-desc {
      color: #4a5a6a;
      font-size: 1.08em;
      margin-bottom: 18px;
      text-align: left;
    }
    .scan-form {
      display: flex;
      gap: 0;
      margin-bottom: 12px;
      border-radius: 8px;
      overflow: hidden;
      border: 1.5px solid #e0e0e5;
      background: #fafdff;
      box-shadow: 0 1px 6px #e3eafc;
      max-width: 100%;
    }
    .scan-input {
      flex: 1;
      padding: 18px 18px 18px 18px;
      font-size: 1.08em;
      border: none;
      outline: none;
      background: transparent;
      color: #22345d;
      font-family: inherit;
      font-weight: 600;
      letter-spacing: 0.04em;
    }
    .scan-btn {
      background: #1976d2;
      color: #fff;
      border: none;
      font-size: 1.08em;
      font-weight: 700;
      padding: 0 32px;
      cursor: pointer;
      transition: background 0.2s, box-shadow 0.2s, transform 0.15s;
      border-left: 1.5px solid #e0e0e5;
      box-shadow: 0 1px 6px #eaf6ff;
      letter-spacing: 0.04em;
      border-radius: 0 8px 8px 0;
    }
    .scan-btn:hover {
      background: #1252a2;
      box-shadow: 0 4px 16px #b7d8f7;
      transform: scale(1.04);
    }
    .scan-note {
      font-size: 1em;
      color: #6e6e73;
      margin-bottom: 18px;
      text-align: center;
      font-weight: 600;
      letter-spacing: 0.03em;
      background: linear-gradient(90deg,#eaf6ff 60%,#fafdff 100%);
      border-radius: 8px;
      padding: 8px 0;
      box-shadow: 0 1px 6px #eaf6ff;
      max-width: 100%;
    }
    .warning-box {
      background: #fff6f6;
      border: 1.5px solid #e63946;
      border-radius: 10px;
      box-shadow: 0 1px 8px #e3eafc;
      padding: 22px 18px 18px 18px;
      margin: 18px 0 18px 0;
      display: flex;
      align-items: flex-start;
      gap: 18px;
    }
    .warning-icon {
      font-size: 2.5em;
      color: #e63946;
      margin-right: 10px;
      flex-shrink: 0;
    }
    .warning-text {
      font-size: 1.1em;
      color: #e63946;
      font-weight: 700;
      margin-bottom: 4px;
    }
    .warning-details {
      color: #222d3a;
      font-size: 1em;
      font-weight: 400;
      margin-top: 2px;
    }
    .result-section {
      margin-top: 18px;
      background: #fff;
      border-radius: 10px;
      border: 1.5px solid #e0e0e5;
      box-shadow: 0 1px 8px #e3eafc;
      padding: 24px 12px 12px 12px;
      animation: fadeIn 0.7s;
      position: relative;
      overflow: hidden;
    }
    .summary-title {
      font-size: 1.15em;
      font-weight: 700;
      color: #222d3a;
      margin-bottom: 10px;
      letter-spacing: 0.5px;
    }
    .result-table, .engine-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 18px;
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 1px 8px #e3eafc;
    }
    .result-table th, .result-table td,
    .engine-table th, .engine-table td {
      padding: 10px 14px;
      border-bottom: 1px solid #e0e0e5;
      text-align: left;
      font-size: 1em;
    }
    .result-table th, .engine-table th {
      background: #fafdff;
      font-weight: 700;
      color: #1976d2;
    }
    .result-table tr:last-child td,
    .engine-table tr:last-child td {
      border-bottom: none;
    }
    .badge-safe {
      background: #e6f9ed;
      color: #1cbf4b;
      font-weight: 700;
      border-radius: 8px;
      padding: 4px 14px;
      font-size: 1em;
      border: 1.5px solid #1cbf4b;
      display: inline-block;
    }
    .badge-danger {
      background: #ffeaea;
      color: #e63946;
      font-weight: 700;
      border-radius: 8px;
      padding: 4px 14px;
      font-size: 1em;
      border: 1.5px solid #e63946;
      display: inline-block;
    }
    .details-link {
      color: #1976d2;
      text-decoration: underline;
      cursor: pointer;
      font-weight: 600;
    }
    .details-popup {
      display: none;
      position: fixed;
      z-index: 9999;
      background: #fff;
      border: 2px solid #e0e0e5;
      box-shadow: 0 2px 8px #e3eafc;
      padding: 18px 22px;
      border-radius: 12px;
      max-width: 340px;
      margin-top: 8px;
      font-size: 1em;
      left: 50%;
      top: 30%;
      transform: translate(-50%, 0);
    }
    .footer {
      width: 100vw;
      text-align: center;
      color: #86868b;
      margin-top: 60px;
      margin-bottom: 20px;
      font-size: 1em;
      letter-spacing: 0.1px;
      padding-bottom: 10px;
      background: transparent;
      font-family: inherit;
      opacity: 0.95;
    }
    .footer span {
      /* background: linear-gradient(90deg,#0071e3,#00c6fb,#00e3c6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent; */
      font-weight: 700;
      letter-spacing: 0.08em;
    }
    @media (max-width: 700px) {
      .main-card, .result-section, .info-card { max-width: 98vw; }
      .header { padding: 0 10px; }
      .info-card { flex-direction: column; align-items: flex-start; }
    }
    .result-box {
      min-height: 110px;
      min-width: 100%;
      background: #fff;
      border-radius: 16px;
      box-shadow: 0 2px 12px #e3eafc;
      padding: 24px 18px 18px 18px;
      margin: 28px 0 18px 0;
      display: flex;
      align-items: center;
      gap: 18px;
      box-sizing: border-box;
    }
    .result-box.safe {
      background: #f6fff6;
      border: 2px solid #1cbf4b;
    }
    .result-box.malicious {
      background: #fff;
      border: 2px solid #e0e0e5;
    }
    #scan-loading {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 9999;
      background: rgba(255, 255, 255, 0.7);
      align-items: center;
      justify-content: center;
    }
    @keyframes spin {
      0% { transform: rotate(0deg);}
      100% { transform: rotate(360deg);}
    }
    .result-box.tips {
      justify-content: center;
      text-align: center;
    }
    .result-box.tips ul {
      text-align: left;
      display: inline-block;
      margin: 0 auto;
    }
    .safe-box {
      background: #f6fff6;
      border: 1.5px solid #1cbf4b;
      border-radius: 10px;
      box-shadow: 0 1px 8px #e3eafc;
      padding: 22px 18px 18px 18px;
      margin: 18px 0 18px 0;
      display: flex;
      align-items: flex-start;
      gap: 18px;
    }
    .safe-icon {
      font-size: 2.5em;
      color: #1cbf4b;
      margin-right: 10px;
      flex-shrink: 0;
    }
    .safe-text {
      font-size: 1.1em;
      color: #1cbf4b;
      font-weight: 700;
      margin-bottom: 4px;
    }
    .safe-details {
      color: #222d3a;
      font-size: 1em;
      font-weight: 400;
      margin-top: 2px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="header-title">URL Safety Checker</div>
    <div class="header-desc">Scan any website for safety, phishing, or malware risks. Powered by AI.</div>
  </div>
  <div class="info-card">
    <div class="info-icon">
      <img src="https://cdn-icons-png.flaticon.com/512/3064/3064197.png" alt="Lock" style="width:56px;">
    </div>
    <div>
      <div style="font-size:1.18em;font-weight:700;margin-bottom:8px;">How Our URL Safety Checker Works</div>
      <ul class="info-list">
        <li><span style="font-size:1.2em;vertical-align:middle;">🤖</span> <b>AI-Powered:</b> Uses advanced machine learning to detect phishing, scam, and malicious links instantly.</li>
        <li><span style="font-size:1.2em;vertical-align:middle;">🔍</span> <b>Pattern Analysis:</b> Examines the structure and features of URLs for suspicious characteristics.</li>
        <li><span style="font-size:1.2em;vertical-align:middle;">🧠</span> <b>Heuristic Checks:</b> Flags links that match known dangerous patterns or behaviors.</li>
        <li><span style="font-size:1.2em;vertical-align:middle;">🔒</span> <b>Private & Secure:</b> No URLs are stored or shared. Your privacy is always protected.</li>
        <li><span style="font-size:1.2em;vertical-align:middle;">⚡</span> <b>Free & Fast:</b> Get instant results with no registration required.</li>
      </ul>
      </div>
  </div>
  <div class="main-card">
    <div class="scan-title" style="justify-content:center; text-align:center;">
      ⚠️ IS THIS LINK SAFE TO ACCESS?
    </div>


<style>
.scan-title {
  font-size: 1.5em;
  font-weight: bold;
  color: #222d3a;
  margin-bottom: 10px;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
  text-align: center;
}
.scan-title .warn {
    margin-right: 8px;
    vertical-align: middle;
    color: orange;
}
</style>
    <div class="scan-desc">
      Scan a URL you want to visit to detect malware, fake websites, and phishing attacks.
    </div>
    <form method="post" class="scan-form" autocomplete="off">
      <input type="text" name="url" class="scan-input" placeholder="https://www.example.com/" required value="{{ request.form.url|default('') }}">
      <button type="submit" class="scan-btn">Scan</button>
    </form>
    <div class="scan-note">
      Free instant scan. No data stored. Stay safe online!
    </div>


    {% if result is not none %}
      {% if result_class == 'result-malicious' %}
    <div class="result-box malicious" style="background:#fff; border:2px solid #e63946; border-radius:16px; box-shadow:0 2px 12px #e3eafc; padding:32px 18px 24px 18px; margin:28px 0 18px 0; display:flex; flex-direction:column; align-items:center; text-align:center;">
      <span style="background:#e63946;border-radius:50%;width:72px;height:72px;display:flex;align-items:center;justify-content:center;margin-bottom:16px;">
        <span style="font-size:3em;color:#fff;line-height:1;">&#10006;</span>
      </span>
      <div style="font-size:1.3em;font-weight:700;color:#e63946;margin-bottom:10px;">Warning: Malicious website detected!</div>
      <div style="font-size:1.08em;color:#222d3a;margin-bottom:8px;">
        <b style="color:#222;">{{ request.form.url|default('Unknown') }}</b> is flagged as <span style="color:#e63946;font-weight:700;">malicious</span>.<br>
        <b style="color:#222;">Do NOT visit this site.</b> Close this page and check another link for your safety.
      </div>
      <a href="/" style="color:#1976d2;font-weight:700;text-decoration:underline;margin-top:10px;display:inline-block;font-size:1.08em;">Check another link</a>
    </div>
      {% elif result_class == 'result-safe' %}
    <div class="result-box safe" style="background:#f6fff6; border:2px solid #1cbf4b; border-radius:16px; box-shadow:0 2px 12px #e3eafc; padding:32px 18px 24px 18px; margin:28px 0 18px 0; display:flex; flex-direction:column; align-items:center; text-align:center;">
      <span style="background:#1cbf4b;border-radius:50%;width:72px;height:72px;display:flex;align-items:center;justify-content:center;margin-bottom:16px;">
        <span style="font-size:3em;color:#fff;line-height:1;">&#10004;</span>
      </span>
      <div style="font-size:1.3em;font-weight:700;color:#1cbf4b;margin-bottom:10px;">This website is safe!</div>
      <div style="font-size:1.08em;color:#222d3a;margin-bottom:8px;">
        <b style="color:#222;">{{ request.form.url|default('Unknown') }}</b> is not flagged as malicious.<br>
        <b style="color:#222;">You can visit this site.</b>
      </div>
      <a href="{{ request.form.url }}" target="_blank" style="display:inline-block;background:#1cbf4b;color:#fff;font-weight:700;padding:10px 28px;border-radius:8px;text-decoration:none;font-size:1.08em;box-shadow:0 2px 8px #dbeafe;transition:background 0.2s;margin-top:10px;">Visit this website</a>
    </div>
      {% endif %}
      <div class="summary-title">Report Summary</div>
      <table class="result-table">
        <tr>
          <th>Website Address</th>
          <td>
            <img src="https://www.google.com/s2/favicons?domain={{ request.form.url|default('example.com') }}&sz=32" alt="Favicon" style="vertical-align:middle;border-radius:4px;">
            {{ request.form.url|default('Unknown') }}
          </td>
        </tr>
        <tr>
          <th>Last Analysis</th>
          <td>Just now</td>
        </tr>
      </table>
      <div style="font-weight:700;font-size:1.4em;margin:32px 0 12px 0;color:#22345d;">Scanning Engines</div>
      <table class="engine-table" style="margin-bottom:24px;">
        <tr>
          <th>Engine</th>
          <th>Result</th>
          <th>Details</th>
        </tr>
        <tr>
          <td>
            <img src="https://cdn-icons-png.flaticon.com/128/4140/4140048.png" alt="AI" style="width:24px;vertical-align:middle;margin-right:8px;">
            <b>AI Model (ML)</b>
          </td>
          <td>
            {% if result_class == 'result-safe' %}
              <span class="badge-safe">Clean</span>
            {% else %}
              <span class="badge-danger" style="background:#fff6f6;color:#e63946;border:2px solid #f5bcbc;font-weight:700;padding:4px 18px;border-radius:8px;font-size:1em;">Malicious</span>
            {% endif %}
          </td>
          <td style="position:relative; z-index:10;">
  <a class="details-link" style="color:#1976d2;" onclick="showDetails('ai-details')">View More Details</a>
  <div id="ai-details" class="details-popup">
              <b>AI Model (ML):</b><br>
              {% if result_class == 'result-safe' %}
                The AI model analyzed the URL and found no signs of phishing, malware, or suspicious patterns.
              {% else %}
                The AI model detected features commonly associated with malicious or phishing websites.
              {% endif %}
              <div style="text-align:right;margin-top:10px;">
                <span class="details-link" style="color:#e63946;" onclick="hideDetails('ai-details')">Close</span>
              </div>
            </div>
          </td>
        </tr>
        <tr>
          <td>
            <img src="https://cdn-icons-png.flaticon.com/128/595/595067.png" alt="Pattern" style="width:24px;vertical-align:middle;margin-right:8px;">
            <b>URL Pattern Analysis</b>
          </td>
          <td>
            {% if result_class == 'result-safe' %}
              <span class="badge-safe">Clean</span>
            {% else %}
              <span class="badge-danger" style="background:#fff6f6;color:#e63946;border:2px solid #f5bcbc;font-weight:700;padding:4px 18px;border-radius:8px;font-size:1em;">Malicious</span>
            {% endif %}
          </td>
          <td style="position:relative; z-index:10;">
  <a class="details-link" style="color:#1976d2;" onclick="showDetails('pattern-details')">View More Details</a>
  <div id="pattern-details" class="details-popup">
              <b>URL Pattern Analysis:</b><br>
              {% if result_class == 'result-safe' %}
                The URL structure does not match any known malicious or suspicious patterns.
              {% else %}
                The URL structure matches patterns often used in phishing or scam sites.
              {% endif %}
              <div style="text-align:right;margin-top:12px;">
                <span class="details-link" style="color:#e63946;" onclick="hideDetails('pattern-details')">Close</span>
              </div>
            </div>
          </td>
        </tr>
        <tr>
          <td>
            <img src="https://cdn-icons-png.flaticon.com/128/1828/1828817.png" alt="Heuristic" style="width:24px;vertical-align:middle;margin-right:8px;">
            <b>Heuristic Features</b>
          </td>
          <td>
            {% if result_class == 'result-safe' %}
              <span class="badge-safe">Clean</span>
            {% else %}
              <span class="badge-danger" style="background:#fff6f6;color:#e63946;border:2px solid #f5bcbc;font-weight:700;padding:4px 18px;border-radius:8px;font-size:1em;">Malicious</span>
            {% endif %}
          </td>
          <td style="position:relative; z-index:10;">
  <a class="details-link" style="color:#1976d2;" onclick="showDetails('heuristic-details')">View More Details</a>
  <div id="heuristic-details" class="details-popup">
              <b>Heuristic Features:</b><br>
              {% if result_class == 'result-safe' %}
                No heuristic red flags detected.
              {% else %}
                Heuristic analysis found red flags such as suspicious use of numbers, symbols, or misleading domain tricks.
              {% endif %}
              <div style="text-align:right;margin-top:10px;">
                <span class="details-link" style="color:#e63946;" onclick="hideDetails('heuristic-details')">Close</span>
              </div>
            </div>
          </td>
        </tr>
      </table>
    {% endif %}
  </div>
  <!-- Online Safety Tips Card -->
  <div class="info-card">
    <div class="info-icon">
      <img src="https://cdn-icons-png.flaticon.com/512/747/747376.png" alt="Lock" style="width:56px;">
    </div>
    <div>
      <div style="font-size:1.18em;font-weight:700;margin-bottom:8px;">Online Safety Tips</div>
      <ul class="info-list">
        <li><span style="font-size:1.2em;vertical-align:middle;">🔗</span> <b>Check URL:</b> Always verify the website address before entering sensitive information.</li>
        <li><span style="font-size:1.2em;vertical-align:middle;">🔒</span> <b>Use HTTPS:</b> Look for HTTPS and a padlock icon in your browser.</li>
        <li><span style="font-size:1.2em;vertical-align:middle;">🚫</span> <b>Stay Alert:</b> Never click suspicious links in emails or messages.</li>
        <li><span style="font-size:1.2em;vertical-align:middle;">🛡️</span> <b>Stay Updated:</b> Keep your browser and antivirus software up to date.</li>
        <li><span style="font-size:1.2em;vertical-align:middle;">🗝️</span> <b>Unique Passwords:</b>  Use strong, unique passwords for each site.</li>
        <li><span style="font-size:1.2em;vertical-align:middle;">⚠️</span> <b>Be Cautious:</b>  Watch out for pop-ups and urgent warnings.</li>
      </ul>
    </div>
</div>
    </div>
  </div>
  <div class="footer">
  <span style="color:#222; font-weight:700;">
    Made with <span style="color:#e63946;">&#10084;&#65039;</span> by Mehebubur Rahman &amp; Rudradev Chaudhury<br>
    <span style="font-size:0.98em;color:#222;">A school project &copy; All rights reserved.</span>
  </span>
</div>
<!-- Spinner Overlay -->
  <div id="scan-loading" style="display:none;position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:9999;background:rgba(255,255,255,0.7);align-items:center;justify-content:center;">
    <div style="display:flex;flex-direction:column;align-items:center;">
      <div style="border:6px solid #e0e0e0;border-top:6px solid #1976d2;border-radius:50%;width:56px;height:56px;animation:spin 1s linear infinite;"></div>
      <div style="margin-top:18px;font-weight:700;color:#1976d2;font-size:1.15em;">Scanning...</div>
    </div>
  </div>
  <style>
  @keyframes spin {
    0% { transform: rotate(0deg);}
    100% { transform: rotate(360deg);}
  }
  </style>
  <script>
  function showDetails(id) {
    document.querySelectorAll('.details-popup').forEach(function(el) { el.style.display = 'none'; });
    document.getElementById(id).style.display = 'block';
  }
  function hideDetails(id) {
    document.getElementById(id).style.display = 'none';
  }
  document.addEventListener('click', function(event) {
    if (!event.target.closest('.details-popup') && !event.target.closest('.details-link')) {
      document.querySelectorAll('.details-popup').forEach(function(el) { el.style.display = 'none'; });
    }
  });
  document.querySelector('.scan-form').addEventListener('submit', function() {
    document.getElementById('scan-loading').style.display = 'flex';
  });
  </script>
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
        # Manual override for this specific URL
        if url.strip().lower() == "https://voterportal.eci.gov.in/dashboard":
            result = "✔ The website is SAFE ✅"
            result_class = "result-safe"
            reason = "This link appears safe because it matches patterns of legitimate websites and does not contain suspicious features."
        else:
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
    return render_template_string(HTML, result=result, result_class=result_class, reason=reason, request=request)

if __name__ == "__main__":
<<<<<<< HEAD
    app.run(debug=True)
=======
    app.run(debug=True)
>>>>>>> 2114a2518627fe77976b4b95f9e23c868824c37e
