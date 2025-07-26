from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from langchain_core.tools import tool
import PyPDF2
import os
import base64


load_dotenv()


OPENAI = os.environ["OPENAI_KEY"]
llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=OPENAI)
@tool
def portfolio_analysi(pdf_file:str):
    """you have to use this tool when you have to analysis portfolio"""
    with open(pdf_file,"rb") as file:
        #reader = PyPDF2.PdfReader(file)
        file.seek(0)
        encoded = base64.b64encode(file.read()).decode("utf-8")
        
    prompt = """You are a recruiter. You have to analyze this pdf file about the portfolio for writing CV and resume.:"""
    message = {
        "role": "user",
        "content": [
            {
                "type":"text",
                "text":prompt,

            },
            {
                "type":"file",
                "source_type":"base64",
                "data":encoded,
                "filename":pdf_file,
                "mime_type":"application/pdf",

            }
        ]}
    prompt = ChatPromptTemplate.from_messages(message)
    chain =  llm | StrOutputParser()
    response = chain.invoke([message])
    print(response)

# if __name__ == '__main__':
#     print("portfolio_analysis start")

#     portfolio_analysi("./Portfolio_채병주_0522.pdf")
#     print("portfolio_analysis end")