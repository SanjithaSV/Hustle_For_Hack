import flask
from flask import request, jsonify
import spacy

app = flask.Flask(__name__)

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model 'en_core_web_sm' not found. Downloading...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

@app.route('/process-report', methods=['POST'])
def process_report():
    """
    Receives a medical report, processes it, and returns a JSON response.
    This endpoint simulates a cloud-based NLP pipeline.
    """
    if not request.json or 'report_text' not in request.json:
        return jsonify({"error": "Missing 'report_text' in request body"}), 400

    report_text = request.json['report_text']

    # Process the text with the NLP model
    doc = nlp(report_text)

    # === Core NLP Logic ===

    # 1. Classification (simulated with keyword matching)
    classification = "General Checkup"
    if any(term in report_text.lower() for term in ["fever", "cough", "infection"]):
        classification = "Respiratory Infection"

    # 2. Keyword/Entity Extraction
    keywords = [ent.text for ent in doc.ents]

    # 3. Summarization (simulated with first three sentences)
    summary = " ".join([sent.text for sent in list(doc.sents)[:3]])

    # 4. Prediction (simulated)
    prediction = "Low risk of chronic disease"
    if "elevated white blood cell count" in report_text.lower():
        prediction = "Moderate risk of inflammation"

    # Prepare the final response
    processed_data = {
        "classification": classification,
        "keywords": keywords,
        "summary": summary,
        "prediction": prediction
    }

    return jsonify(processed_data)

if __name__ == '__main__':
    # Run the server on localhost, for local testing
    app.run(debug=True, port=5000)