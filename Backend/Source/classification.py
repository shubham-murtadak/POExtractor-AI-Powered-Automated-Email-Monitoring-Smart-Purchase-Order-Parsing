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


#create instance of llm model 
# llm= ChatGoogleGenerativeAI(model='gemini-1.5-pro',google_api_key="AIzaSyD-XmZVwlrHO_SqOM0qzHx9eUF_t6WfuUI",temperature=0)
# llm= ChatGoogleGenerativeAI(model='gemini-1.5-pro',google_api_key=GEMINI_API_KEY,temperature=0)

llm= ChatGroq(model="mixtral-8x7b-32768",temperature=0,max_tokens=None,timeout=None,max_retries=2,api_key=GROQ_API_KEY)


# Function To Get Single Source Responses
def classify_email(subject,body):
 
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
    # while(True):
        # doctype=input('select your doctype :')
        # doclist=[doctype]
        # question=input("Enter your question :")
        # if(question=='break'):
        #     break

    # subject = "Purchase Order"
    # body = """
    # Dear Mam,

    # Please find attached herewith our Purchase Order.

    # Regards,

    # Mamta

    # ---

    # Aakash Ele (India)
    # 308, K. K. Gupta Ind. Est.,
    # R. P. Road,
    # Mulund (W)
    # Mumbai-400 080

    # One attachment - Scanned by Gmail
    # """
    # subject = "Required packing slip on polybag & box"
    # body = """
    # Dear Sir,

    # We have to inform you that at inward inspection time the packing slip on the polybag & box not receive in your material as per attached images for your references.

    # So implement this on priority in the next lot otherwise we will not accept the material for inward.

    # Regards,
    # """

    # subject = "Re: VF-161/2024/10/30 RFQ-EM69551/EM69125"
    # body = """
    # Dear sir,

    # Please inform status of quotation No: VF-161/2024/10/30

    # Thanks & Regards,

    # AASHA

    # On Tue, Nov 5, 2024 at 12:49 PM <sales@vaishnavfastners.com> wrote:
    # Dear sir,

    # Please inform status of quotation No: VF-161/2024/10/30

    # Thanks & Regards,

    # Anjul Shrivastav

    # 11/12, Sethia Industrial Park,
    # """
    # 
    subject = "Re: Re: Re: VF-161/2024/10/30 RFQ-EM69551/EM69125"
    body = """Dear Sir, 
    Please find attached herewith Quotation No: VF-161/2024/10/30 for your reference.

    Thanks & Regards, 
    Aasha

    On Tue, Oct 22, 2024 at 12:35 PM Zodge <[email protected]> wrote: 
    Dear Sir, PFA drawing, Kindly share the quotation along with MOQ. 
    BR/T Zodge 

    On Tue, Nov 5, 2024 at 12:49 PM sales@vaishnavfastners.com <https://www.google.com/url?sa=E&source=gmail&q=mailto:sales@vaishnavfastners.com> wrote: 
    Dear sir, Please inform status of quotation No: VF-161/2024/10/30 
    Thanks & Regards, 
    Anjul Shrivastav 
    11/12, Sethia Industrial Park, 

    On Thu, Nov 7, 2024 at 3:09 PM Aasha wrote: 
    Dear Sir, Please inform status of quotation No: VF-161/2024/10/30 
    Thanks & Regards, 
    Aasha
    """


    # subject="Purchase Order"
    # body="Dear Mam, Please find attached herewith our Purchase Order.Regards,Mamta"
    ans=classify_email(subject,body)
    # print(ans)
    print()

    # history=get_session_history('panks87')



