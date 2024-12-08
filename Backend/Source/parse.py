import os
import json 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from typing import Tuple, List, Optional
from dotenv import load_dotenv
from llama_parse import LlamaParse  # changes
from langchain_groq import ChatGroq
from langchain_google_genai import (ChatGoogleGenerativeAI,HarmBlockThreshold,HarmCategory,)
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import (RunnableBranch,RunnableLambda,RunnableParallel,RunnablePassthrough)
from operator import itemgetter
from langchain_core.documents import Document
from openpyxl import load_workbook
from langchain_community.document_loaders import UnstructuredExcelLoader
#loading env variables 
load_dotenv()


#loading environment variables 
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
GROQ_API_KEY=os.getenv('GROQ_API_KEY')
PROJECT_HOME_PATH=os.getenv('PROJECT_HOME_PATH')
LLAMA_CLOUD_API_KEY=os.getenv('LLAMA_CLOUD_API_KEY')

#create instance of llm model 
llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro', google_api_key=GEMINI_API_KEY, temperature=0)

#define gemini embeddings
gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)

def parsed_pdf_data(pdf_path):
    """
    * method: parsed_pdf_data
    * description: Method to parse a provided PDF file (purchase order) and extract specified fields into a structured JSON format.
    * return: Parsed JSON data as a Python dictionary containing purchase order details.
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * Shubham M        07-DEC-2024    1.0      initial creation
    *
    * Parameters
    *   pdf_path (str): The path to the PDF file to be parsed.
    """

    # Define the instruction for LlamaParser
    instruction = """
        You are a PDF parser specializing in purchase orders. Your task is to extract the following fields from the document and structure them into a JSON format. Ensure all mandatory fields are always present, and optional fields are included only if available.

        ### Instructions:
        1. Carefully parse the provided purchase order PDF to extract the specified fields.
        2. Return the parsed data as a JSON object strictly adhering to the schema below.
        3. For any field marked as "optional" that cannot be found, leave its value as an empty string ("").
        4. Ensure accurate mapping of item details, delivery dates, and other PO information.

        ### Required Fields and Output JSON Schema:
        ```json
        {
        "Customer_PO_Number": "<string>",
        "Customer_Name": "<string>",
        "Customer_Details": {
            "Phone_Number": "<string>",
            "Email": "<string>",
            "GST_Number": "<string>"
        },
        "Items": [
            {
            "Item_Name": "<string>",
            "Quantity": "<string>",
            "Rate_per_Unit": "<string>",
            "Unit_of_Measurement": "<string>",
            "Delivery_Dates": "<string>"
            }
        ],
        "Applicable_Taxes": "<string>",
        "Terms_of_Payment": "<string>",
        "Discount": "<string>",
        "Other_Remarks_or_Instructions": "<string>"
        }
        """

    # Use LlamaParse to extract the data
    parsed_data = LlamaParse(result_type="markdown", api_key=LLAMA_CLOUD_API_KEY,
                             parsing_instruction=instruction).load_data(pdf_path)

    ## Access the text of the first Document in the list
    if parsed_data:
        document_text = parsed_data[0].text  # Adjust the index if there are multiple documents
    else:
        document_text="{}"

    # Remove the triple-backticks and newlines for JSON parsing
    clean_text = document_text.strip("```json\n").strip("```")

    # Convert the JSON string to a Python dictionary
    try:
        data_dict = json.loads(clean_text)
        # print("data dict is :")
        # print(data_dict)
    except json.JSONDecodeError as e:
        data_dict={}
        print("Failed to parse JSON:", e)
    
    return data_dict

def parsed_excel_data(excel_path):
    """
    * method: parsed_excel_data
    * description: Method to parse a provided Excel file (purchase order data) and extract specified fields into a structured JSON format.
    * return: Parsed JSON data as a Python dictionary containing purchase order details.
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * Shubham M        07-DEC-2024     1.0      initial creation
    *
    * Parameters
    *   excel_path (str): The path to the Excel file to be parsed.
    """

    loader = UnstructuredExcelLoader(excel_path, mode="elements")
    docs = loader.load()
    print(len(docs))

    parsed_data=[]
    for doc in docs:
        parsed_data.append(doc.page_content)
    
    # print(parsed_data)
    # docs=[page[0].content for page in docs]

    ss_template = """
        You are a purchase order parser specializing in extracting details from Excel files. Your task is to extract the following fields from the provided purchase order data and structure them into a JSON format. Ensure all mandatory fields are always present, and optional fields are included only if available.

        ### Instructions:
        1. Carefully parse the provided purchase order Excel data to extract the specified fields.
        2. Return the parsed data as a JSON object strictly adhering to the schema below.
        3. For any field marked as "optional" that cannot be found, leave its value as an empty string ("").
        4. Ensure accurate mapping of item details, delivery dates, and other PO information.

        ### Required Fields and Output JSON Schema:
                ```json
                {{
                "Customer_PO_Number": "<string>",
                "Customer_Name": "<string>",
                "Customer_Details": {{
                    "Phone_Number": "<string>",
                    "Email": "<string>",
                    "GST_Number": "<string>"
                }},
                "Items": [
                    {{
                    "Item_Name": "<string>",
                    "Quantity": "<string>",
                    "Rate_per_Unit": "<string>",
                    "Unit_of_Measurement": "<string>",
                    "Delivery_Dates": "<string>"
                    }}
                ],
                "Applicable_Taxes": "<string>",
                "Terms_of_Payment": "<string>",
                "Discount": "<string>",
                "Other_Remarks_or_Instructions": "<string>"
                }}
                ```
        Excel_data:{data}
"""

    
    QA_PROMPT=PromptTemplate(
        template=ss_template,
        input_variables=["data"]
    )

    chain=(
        {
        "data":itemgetter("data")
        }
        |QA_PROMPT
        |llm
    )
    
    try:
        # result=conversational_rag_chain.invoke({"question": question,"no_of_classes":no_of_classes,"class_list":class_list,"context":docs})
        result=chain.invoke({"data":parsed_data})
        # print("result is :",result)
        result=result.content

         # Remove the triple-backticks and newlines for JSON parsing
        clean_text = result.strip("```json\n").strip("```")

        # Convert the JSON string to a Python dictionary
        try:
            data_dict = json.loads(clean_text)
            # print("data dict is :")
            # print(data_dict)
        except json.JSONDecodeError as e:
            data_dict={}
            print("Failed to parse JSON:", e)

        return data_dict
    except  Exception as e:
        print(f"Error: {e}")
    
if __name__=='__main__':
    pdf_path="D://personal//Personal Projects//POExtractor//Backend//Data//Extract_data//shubhammurtadak022_gmail_com_2024-12-07_13-07-51//60 - Vaishnav - 25.06.2024 (MO screw).xlsx"
    parsed_data=parsed_excel_data(pdf_path)
    print(parsed_data)

    
    







