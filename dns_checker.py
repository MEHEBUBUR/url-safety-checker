# dns_checker.py
import joblib

def main():
    try:
        # Load trained model and vectorizer
        model = joblib.load('D:/project/url/model.pkl')
        vectorizer = joblib.load('D:/project/url/vectorizer.pkl')
    except Exception as e:
        print(f"Error loading model or vectorizer: {e}")
        return

    # Get URL input
    url = input("🔎 Enter the website URL to check: ").strip()

    try:
        # Predict
        url_vec = vectorizer.transform([url])
        prediction = model.predict(url_vec)[0]
    except Exception as e:
        print(f"Error during prediction: {e}")
        return

    # Show result
    if prediction == 'benign':
        print("✔ The website is SAFE ✅")
    else:
        print("❌ The website is MALICIOUS 🚫")

if __name__ == "__main__":
    main()
