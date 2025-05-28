# URL Safety Checker

URL Safety Checker is a web application that helps users verify the safety of URLs before visiting them. This tool analyzes URLs for potential security threats such as phishing, malware, and scams.

## Features

- Real-time URL analysis
- Comprehensive security checks
- Risk scoring system
- Detailed threat information
- Mobile-friendly design
- Educational resources on cybersecurity

## Deployment Instructions

### Local Development

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```

### Heroku Deployment

1. Install the Heroku CLI from [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to Heroku:
   ```
   heroku login
   ```
3. Create a new Heroku app:
   ```
   heroku create urlsafetychecker
   ```
   (or choose your own unique app name)
4. Deploy the application:
   ```
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```
5. Open the deployed application:
   ```
   heroku open
   ```

## Technologies Used

- Python
- Flask
- HTML/CSS/JavaScript
- Bootstrap

## Note

This is an educational project that demonstrates URL safety checking concepts. For mission-critical security, consider using professional cybersecurity solutions. 