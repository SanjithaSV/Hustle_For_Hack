import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from database import get_db_connection

def get_data_for_ml():
    # Fetch data from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT report_text, category FROM reports")
    data = cursor.fetchall()
    conn.close()
    
    # Convert data to pandas DataFrame
    df = pd.DataFrame(data, columns=["report_text", "category"])
    return df

def train_ml_model():
    # Get data from the database
    df = get_data_for_ml()
    
    # Define the TF-IDF vectorizer and classifier
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["report_text"])
    y = df["category"]
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train a RandomForest classifier
    classifier = RandomForestClassifier()
    classifier.fit(X_train, y_train)
    
    # Predictions and evaluation
    y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # Save the trained model (optional)
    import joblib
    joblib.dump(classifier, "report_classifier_model.pkl")
    joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

# Run the model training
if __name__ == "__main__":
    train_ml_model()
