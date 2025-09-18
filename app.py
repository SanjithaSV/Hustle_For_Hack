from flask import Flask, render_template, request, jsonify
from insert_data import insert_report
from ml_model import predict_report_category
from database import get_db_connection

app = Flask(__name__)

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
        
        # Get the prediction from the ML model
        predicted_category = predict_report_category(report_text)
        
        return render_template('index.html', prediction=predicted_category)

if __name__ == "__main__":
    app.run(debug=True)
