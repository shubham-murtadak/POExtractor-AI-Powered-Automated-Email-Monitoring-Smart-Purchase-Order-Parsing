import os
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


#loading env variables 
load_dotenv()
#loading environment variables 
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
GROQ_API_KEY=os.getenv('GROQ_API_KEY')
PROJECT_HOME_PATH=os.getenv('PROJECT_HOME_PATH')
LLAMA_CLOUD_API_KEY=os.getenv('LLAMA_CLOUD_API_KEY')


llm= ChatGroq(model="mixtral-8x7b-32768",temperature=0,max_tokens=None,timeout=None,max_retries=2,api_key=GROQ_API_KEY)


# Function To Get Single Source Responses
def classify_email(subject,body):
    """
    * method: classify_email
    * description: Method to classify an email as either a purchase order-related email ("Yes") or not ("No") based on the subject and body.
    * return: JSON response with classification ("Yes" or "No") and confidence percentage.
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * Shubham M      08-DEC-2024       1.0      initial creation
    *
    * Parameters
    *   subject (str): The subject of the email.
    *   body (str): The body content of the email.
    """

 
    # Dynamic Prompt
    ss_template = """
    Analyze the provided email details to determine if it contains a request or reference to a purchase order (PO) or similar procurement-related instructions.  
    Your task is to classify the email as either "Yes" or "No" and provide a confidence percentage.

    Follow these instructions:
    1. Classify the email as "Yes" if it explicitly mentions or implies:
    - A request for a purchase order (PO).
    - Classify the email as a purchase order only if it explicitly contains an order for goods or services, including specific quantities, pricing, and delivery terms.
    - Instructions or details related to procurement, supply, or dispatch planning.
    - Acknowledgment or confirmation requests for procurement-related matters.
    
    2. If none of the above criteria are met, classify it as "No."

    3. Output must strictly adhere to the following JSON format:
        {{
            "classification": "Yes" or "No",
            "confidence": <percentage>(do not add'%' sign only number eg.99)
        }}

    4. Do not include any explanations, descriptions, or additional content—output only the JSON response.

    Email Subject: {subject}

    Email Body: {body}

    Output:

"""



    QA_PROMPT=PromptTemplate(
        template=ss_template,
        input_variables=["subject","body"]
    )

    rag_chain=(
        {
        "subject":itemgetter("subject"),
        "body":itemgetter("body")
        }
        |QA_PROMPT
        |llm
    )
    
    try:
            # result=conversational_rag_chain.invoke({"question": question,"no_of_classes":no_of_classes,"class_list":class_list,"context":docs})
            result=rag_chain.invoke({"subject":subject,"body":body})
            # print("result is :",result)
            result=result.content
            print()
            print(result)
            print()
            return result
    except  Exception as e:
        print(f"Error: {e}")

if __name__=='__main__':
    subject="Purchase Order"
    body="Dear Mam, Please find attached herewith our Purchase Order.Regards,Mamta"
    ans=classify_email(subject,body)


