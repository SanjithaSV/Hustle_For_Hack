import logging
import warnings
import sys
import csv
import fitz  # PyMuPDF
import re
import medspacy

# Suppress warnings and debug logs
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.WARNING)

nlp = medspacy.load()

class DummyFile(object):
    def write(self, x): pass

def silent_nlp(text):
    saved_stdout = sys.stdout
    sys.stdout = DummyFile()
    try:
        doc = nlp(text)
    finally:
        sys.stdout = saved_stdout
    return doc

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening file: {e}")
        return ""
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_lab_values(text):
    pattern = re.compile(r"([A-Za-z\s/-]+)[:\-]?\s*([\d\.]+)", re.IGNORECASE)
    results = pattern.findall(text)
    lab_dict = {}
    for name, value in results:
        clean_name = name.strip().title()
        lab_dict[clean_name] = value
    return lab_dict

def save_lab_results_csv(lab_dict, filename="lab_results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Lab Test", "Value"])
        for test, value in lab_dict.items():
            writer.writerow([test, value])
    print(f"Lab results saved to {filename}")

def extract_medical_entities(text):
    doc = silent_nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def keyword_entity_extraction(text, keywords):
    found = []
    for kw in keywords:
        if kw.lower() in text.lower():
            found.append((kw, "Keyword"))
    return found

def main():
    pdf_path = input("Enter full path to PDF medical report: ")
    extracted_text = extract_text_from_pdf(pdf_path)

    if not extracted_text:
        print("No text extracted from PDF or error opening file.")
        return

    print("\nLab Test Results:")
    labs = extract_lab_values(extracted_text)
    if labs:
        for test, value in labs.items():
            print(f"{test}: {value}")
        save_lab_results_csv(labs)
    else:
        print("No lab test values found.")

    print("\nMedical Entities (NLP):")
    entities = extract_medical_entities(extracted_text)
    if entities:
        for ent_text, ent_label in entities:
            print(f"{ent_text} ({ent_label})")
    else:
        print("No medical entities found with NLP.")

    keywords = ["dementia", "stroke", "hypertension", "cardiomyopathy", "renal disease"]
    keyword_entities = keyword_entity_extraction(extracted_text, keywords)
    if keyword_entities:
        print("\nKeyword-based detections:")
        for kw, label in keyword_entities:
            print(f"{kw} ({label})")
    else:
        print("No keyword matches found.")

if __name__ == "__main__":
    main()
