import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.MEDBOT.utils import read_file, get_structured_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.MEDBOT.MedBot import generate_evaluate_chain
from src.MEDBOT.logger import logging

# Load environment variables
load_dotenv()


def customize_ui_elements():
    st.markdown(
        """
        <style>
            .stApp {
                background-image: linear-gradient(to top, #30cfd0 0%, #330867 100%);
            }
            button {
                border: none;
                color: white;
                background-color: #1E88E5;
            }
            .stFileUploader {
                border-color: #1E88E5;
                color: #1E88E5;
                background-color: #ffffff;
            }
            .stTextInput input, .stNumberInput input {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #1E88E5;
            }
            .stSelectbox select {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #1E88E5;
            }
            .st-btn-primary {
                background-color: #1E88E5;
                border: none;
                color: white;
            }
            .stSlider .thumb {
                background-color: #1E88E5;
            }
            .stSlider .track {
                background-color: #D1D1D1;
            }
            .stRadio > label, .stCheckbox > label {
                background-color: #ffffff;
                border: 1px solid #1E88E5;
                color: #000000;
                border-radius: 4px;
                padding: 5px 10px;
            }
            .stSelectbox > div > div {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            .stSelectbox > div > ul > li {
                color: #000000 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def json_to_markdown(json_data):
    try:
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        if not json_data:
            return "No data available"
        markdown_str = json.dumps(json_data, indent=2)
        return f"```json\n{markdown_str}\n```"
    except Exception as e:
        logging.error(f"Error converting JSON to Markdown: {e}")
        return {"ERROR": {"message": str(e)}}


customize_ui_elements()

with open("Response.json", "r") as file1:
    RESPONSE_JSON = json.load(file1)

st.markdown("<h1 style='text-align: center; color: white;'>Gaia: Medical Data Extraction and Analysis</h1>", unsafe_allow_html=True)


uploaded_file = st.file_uploader("Upload a PDF or txt file or a jpg file")


button = st.button("Process Clinical Notes")
    
    
if button and uploaded_file is not None:
    with st.spinner("Processing..."):
        try:
            text = read_file(uploaded_file)
            with get_openai_callback() as cb:
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "query": "Hello",
                        "response_json": json.dumps(RESPONSE_JSON),
                    }
                )
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error processing the clinical notes")
        else:
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost: {cb.total_cost}")

            try:
                response_dict = response
            except json.JSONDecodeError as e:
                st.error("Error decoding the response JSON")
                traceback.print_exception(type(e), e, e.__traceback__)
                response_dict = {}

            output1 = response_dict.get("output1", {})

            if output1:
                # Convert to DataFrame
                structured_data_df = json_to_markdown(output1)

                st.subheader("Structured Data")
                st.markdown(structured_data_df)

            else:
                st.error("Error in the response data")


query = st.text_input("Enter the Query", max_chars = 100)
button = st.button("Ask Query")
    
if button and query and uploaded_file is not None:
    with st.spinner("Processing..."):
        try:
            text = read_file(uploaded_file)
            with get_openai_callback() as cb:
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "query": query,
                        "response_json": json.dumps(RESPONSE_JSON),                        }
                )
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error processing the clinical notes")
        else:
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost: {cb.total_cost}")

            try:
                response_dict = response
            except json.JSONDecodeError as e:
                st.error("Error decoding the response JSON")
                traceback.print_exception(type(e), e, e.__traceback__)
                response_dict = {}

            output1 = response_dict.get("output1", {})
            output2 = response_dict.get("output2", {})

            if output1 and output2:
                # Convert to DataFrame
                structured_data_df = json_to_markdown(output1)
                
                st.subheader("Response")
                st.write(output2)

            else:
                st.error("Error in the response data")