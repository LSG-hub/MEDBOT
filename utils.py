import os
import PyPDF2
import json
import traceback
from PIL import Image

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error reading the PDF file") from e
    elif file.name.endswith(".txt"):
        try:
            return file.read().decode("utf-8")
        except Exception as e:
            raise Exception("Error reading the TXT file") from e
        
    else:
        raise Exception("Unsupported file format. Only .pdf, .txt files and .jpg are supported")

def get_structured_data(json_str):
    try:
        data_dict = json.loads(json_str)
        structured_data = {
            "Patient Information": data_dict.get("Patient Information", {}),
            "Chief Complaint": data_dict.get("Chief Complaint", ""),
            "History of Present Illness": data_dict.get("History of Present Illness", ""),
            "Past Medical History": data_dict.get("Past Medical History", ""),
            "Medications": data_dict.get("Medications", ""),
            "Allergies": data_dict.get("Allergies", ""),
            "Family History": data_dict.get("Family History", ""),
            "Social History": data_dict.get("Social History", ""),
            "Review of Systems": data_dict.get("Review of Systems", ""),
            "Physical Examination": data_dict.get("Physical Examination", {}),
            "Diagnostic Workup": data_dict.get("Diagnostic Workup", ""),
            "Assessment and Plan": data_dict.get("Assessment and Plan", "")
        }
        return structured_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

