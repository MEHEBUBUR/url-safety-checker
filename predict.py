# predict.py
import joblib

def main():
    try:
        # Load saved model and vectorizer
        model = joblib.load('D:/project/url/model.pkl')
        vectorizer = joblib.load('D:/project/url/vectorizer.pkl')
    except Exception as e:
        print(f"Error loading model or vectorizer: {e}")
        return

    # Input URL for prediction
    url = input("Enter a URL to check if it's malicious: ").strip()

    try:
        # Transform and predict
        url_vec = vectorizer.transform([url])
        prediction = model.predict(url_vec)
        print(f"🚨 The URL is classified as: {prediction[0]}")
    except Exception as e:
        print(f"Error during prediction: {e}")

if __name__ == "__main__":
    main()
