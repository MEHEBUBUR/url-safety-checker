print("Script started")  # Add this line

# main.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def main():
    # Load your combined dataset
    df = pd.read_csv('D:/project/dataset/combined_dataset.csv')
    print("CSV loaded, shape:", df.shape)

    # Map target to label: 'benign' or 'malicious'
    df['label'] = df['target'].apply(lambda x: 'benign' if str(x).lower() == 'benign' else 'malicious')

    # After loading and labeling your DataFrame:
    benign_df = df[df['label'] == 'benign']
    malicious_df = df[df['label'] == 'malicious']
    min_count = min(len(benign_df), len(malicious_df))
    df = pd.concat([
        benign_df.sample(min_count, random_state=42),
        malicious_df.sample(min_count, random_state=42)
    ]).sample(frac=1, random_state=42)

    # Features and labels
    X = df['url']
    y = df['label']

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)
    print("TF-IDF vectorization complete.")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
    print("Data split complete.")

    # Model training
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    print("Model training complete.")

    # Evaluation
    print(classification_report(y_test, model.predict(X_test)))

    # Save model and vectorizer
    joblib.dump(model, 'D:/project/url/model.pkl')
    joblib.dump(vectorizer, 'D:/project/url/vectorizer.pkl')
    print("✅ Model trained and saved.")

if __name__ == "__main__":
    main()

    