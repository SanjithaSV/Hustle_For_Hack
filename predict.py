import joblib

# Load the saved model and vectorizer
model = joblib.load("report_classifier_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def predict_report_category(report_text):
    # Transform the text into TF-IDF features
    X_new = vectorizer.transform([report_text])
    
    # Predict category using the trained model
    prediction = model.predict(X_new)
    return prediction[0]

# Example Prediction
if __name__ == "__main__":
    report_text = "Patient shows severe chest pain and discomfort."
    category = predict_report_category(report_text)
    print(f"Predicted Category: {category}")
