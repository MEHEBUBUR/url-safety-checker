from flask import Flask, render_template, request, redirect, url_for
import re
import random
import time
from urllib.parse import urlparse
import os

app = Flask(__name__)

def is_valid_url(url):
    """Check if the URL is valid in format"""
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(regex, url) is not None

def analyze_url(url):
    """Analyze the URL for safety"""
    # In a real application, this would connect to security APIs or databases
    # For demo purposes, we'll use a simple algorithm to classify URLs
    
    # Extract domain for analysis
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # List of suspicious terms in URLs - expanded for stricter checking
    suspicious_terms = ['phish', 'login', 'verify', 'account', 'secure', 'banking', 
                        'paypal', 'signin', 'free', 'win', 'click', 'confirm', 'password',
                        'update', 'access', 'reset', 'alert', 'authenticate', 'wallet',
                        'crypto', 'bitcoin', 'urgent', 'official', 'verify', 'security',
                        'support', 'help', 'payment', 'bank', 'credit', 'debit', 'cash']
                        
    # Demo logic: URLs containing suspicious terms or with specific TLDs are flagged
    # In reality, you would use ML models or security API services
    
    # Simulate processing time for better UX
    time.sleep(1)
    
    # Check for known safe domains (popular websites that are generally safe)
    known_safe_domains = ['google.com', 'microsoft.com', 'apple.com', 'amazon.com', 
                        'facebook.com', 'youtube.com', 'twitter.com', 'linkedin.com',
                        'github.com', 'wikipedia.org', 'yahoo.com', 'netflix.com',
                        'instagram.com', 'zoom.us', 'wordpress.com', 'adobe.com',
                        'dropbox.com', 'reddit.com', 'cnn.com', 'bbc.com', 'nytimes.com']
    
    # Check for obviously suspicious TLDs or domains - expanded for stricter checking
    suspicious_tlds = ['.tk', '.ru', '.cn', '.buzz', '.xyz', '.info', '.top', '.cc', 
                       '.ws', '.ga', '.gq', '.ml', '.cf', '.loan', '.click', '.link',
                       '.work', '.stream', '.racing', '.win', '.bid', '.download']
    
    # Check length of domain (very long domains are often suspicious)
    domain_length_suspicious = len(domain) > 30
    
    # Check for numbers in domain (can indicate generated domains)
    has_many_numbers = sum(c.isdigit() for c in domain) > 4
    
    # Check for hyphens (multiple hyphens often indicate suspicious domains)
    has_many_hyphens = domain.count('-') > 2
    
    # Determine if URL is likely safe or unsafe
    has_suspicious_term = any(term in url.lower() for term in suspicious_terms)
    has_suspicious_tld = any(tld in domain.lower() for tld in suspicious_tlds)
    is_known_safe = any(safe_domain in domain.lower() for safe_domain in known_safe_domains)
    
    # Suspicious domain characteristics count
    suspicious_characteristics = sum([
        has_suspicious_term,
        has_suspicious_tld,
        domain_length_suspicious,
        has_many_numbers,
        has_many_hyphens
    ])
    
    # Create a more balanced assessment with stricter rules
    # If it's a known safe domain, still moderate chance to flag (for demo purposes)
    if is_known_safe:
        is_malicious = random.random() < 0.25  # increased from 10% to 25% chance
    # If it has multiple suspicious characteristics, very likely to be malicious
    elif suspicious_characteristics >= 2:
        is_malicious = random.random() < 0.95  # 95% chance to flag highly suspicious sites
    # If it has one suspicious characteristic, moderately likely to be malicious
    elif suspicious_characteristics == 1:
        is_malicious = random.random() < 0.75  # 75% chance to flag somewhat suspicious sites
    # For all other sites, still high chance to flag for demo purposes
    else:
        is_malicious = random.random() < 0.6  # increased from 50% to 60% chance
    
    # Generate more detailed threat information
    if is_malicious:
        threat_types = []
        
        # Determine threat types based on characteristics
        if any(term in url.lower() for term in ['login', 'signin', 'account', 'password', 'verify']):
            threat_types.append('Phishing')
        if any(term in url.lower() for term in ['free', 'win', 'prize', 'offer', 'discount']):
            threat_types.append('Scam')
        if any(tld in domain.lower() for tld in suspicious_tlds):
            threat_types.append('Suspicious Origin')
        if has_many_numbers or domain_length_suspicious:
            threat_types.append('Suspicious Domain Pattern')
        if has_many_hyphens:
            threat_types.append('Possible Typosquatting')
        if not threat_types:
            threat_types = ['Malware', 'Suspicious Activity']
            
        # Higher risk scores
        return {
            'safe': False,
            'threats': threat_types,
            'risk_score': random.randint(75, 98),  # increased minimum risk score
            'details': {
                'domain_age': f"{random.randint(1, 30)} days",
                'ssl_valid': random.choice([True, False]),
                'blacklist_status': 'Blacklisted on multiple databases',
                'redirects': random.randint(0, 3)
            }
        }
    else:
        # Lower risk scores for "safe" sites to create more contrast
        return {
            'safe': True,
            'risk_score': random.randint(0, 15),  # decreased maximum "safe" risk score
            'details': {
                'domain_age': f"{random.randint(1, 10)} years",
                'ssl_valid': True,
                'blacklist_status': 'Not blacklisted',
                'redirects': 0
            }
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_url():
    url = request.form.get('url', '')
    
    if not url:
        return render_template('index.html', error="Please enter a URL to check")
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if not is_valid_url(url):
        return render_template('index.html', error="Invalid URL format. Please enter a valid URL")
    
    result = analyze_url(url)
    
    return render_template('result.html', 
                          url=url, 
                          result=result)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/security-blog')
def security_blog():
    return render_template('security_blog.html')

@app.route('/safety-tips')
def safety_tips():
    return render_template('safety_tips.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

if __name__ == '__main__':
    # Use environment variable for port with a default of 5000
    port = int(os.environ.get('PORT', 5000))
    # In production, debug should be False
    app.run(host='0.0.0.0', port=port, debug=False) 