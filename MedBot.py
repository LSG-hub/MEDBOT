import os
import json
import pandas as pd
import traceback #type: ignore
from dotenv import load_dotenv
from src.MEDBOT.utils import read_file, get_structured_data
from src.MEDBOT.logger import logging

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key = key, model_name = "gpt-3.5-turbo", temperature = 1.0)

TEMPLATE = """
Text: {text}
You are an expert in medical data extraction. Given the above unstructured clinical notes, your task is to convert them into structured data. Extract and organize the information under the following categories:

1. Patient Information:
   - Patient ID
   - Name
   - Age
   - Gender

2. Chief Complaint:
   - Description

3. History of Present Illness:
   - Description

4. Past Medical History:
   - Description

5. Medications:
   - Description

6. Allergies:
   - Description

7. Family History:
   - Description

8. Social History:
   - Description

9. Review of Systems:
   - Description

10. Physical Examination:
    - Vital Signs
    - HEENT
    - Neck
    - Cardiovascular
    - Respiratory
    - Gastrointestinal
    - Genitourinary
    - Neurological
    - Musculoskeletal
    - Skin

11. Diagnostic Workup:
    - Description

12. Assessment and Plan:
    - Description

Make sure to format your response like RESPONSE_JSON below and use it as a guide.
### RESPONSE_JSON
{response_json}

"""

response_generation_prompt = PromptTemplate(
    input_variables = ["text", "response_json"],
    template = TEMPLATE
)

response_chain_1 = LLMChain(llm = llm, prompt = response_generation_prompt, output_key = "output1", verbose = True)

SUGGESTIONS_TEMPLATE = """
Text: {text}
You are an expert in medical data analysis named Sreenivas. Given the above unstructured clinical notes, your task is to completely analyze the data in detail and the user query asked below.

Query: {query}

Send a very detailed answer to the query asked in a friendly manner as a wellwisher and caretaker. Make sure the query is not in the form of any letter and is a casual response.

"""

suggestion_generation_prompt = PromptTemplate(
    input_variables = ["text", "query"],
    template = SUGGESTIONS_TEMPLATE
)

response_chain_2 = LLMChain(llm = llm, prompt = suggestion_generation_prompt, output_key = "output2", verbose = True)

generate_evaluate_chain = SequentialChain(chains = [response_chain_1, response_chain_2], input_variables = ["text", "response_json", "query"], output_variables = ["output1", "output2"], verbose = True)

