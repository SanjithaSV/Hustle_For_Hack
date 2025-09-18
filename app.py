from flask import Flask, render_template, request, jsonify
import spacy
from database import get_db_connection
from insert_data import insert_report

app = Flask(_name_)

# Load the spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model 'en_core_web_sm' not found. Downloading...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert_report', methods=['POST'])
def insert_new_report():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        report_text = request.form['report_text']
        summary = request.form['summary']
        category = request.form['category']
        prediction = request.form['prediction']
        
        # Insert the report into the database
        insert_report(patient_id, report_text, summary, category, prediction)
        
        return render_template('index.html', message="Report inserted successfully!")

@app.route('/predict', methods=['POST'])
def predict_category():
    if request.method == 'POST':
        report_text = request.form['report_text']
        
        # Process the text with the NLP model
        doc = nlp(report_text)
        
        # Classification (simulated with keyword matching)
        classification = "General Checkup"
        if any(term in report_text.lower() for term in ["fever", "cough", "infection"]):
            classification = "Respiratory Infection"
        
        # Keyword/Entity Extraction
        keywords = [ent.text for ent in doc.ents]
        
        # Summarization (simulated with first three sentences)
        summary = " ".join([sent.text for sent in list(doc.sents)[:3]])
        
        # Prediction (simulated)
        prediction = "Low risk of chronic disease"
        if "elevated white blood cell count" in report_text.lower():
            prediction = "Moderate risk of inflammation"
        
        return render_template('index.html', 
                              prediction=prediction,
                              classification=classification,
                              keywords=keywords,
                              summary=summary)

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

if _name_ == "_main_":
    app.run(debug=True, port=5000)
