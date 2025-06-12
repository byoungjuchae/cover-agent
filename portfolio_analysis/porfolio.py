from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import PyPDF2
import os
import base64


load_dotenv()


# os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
# os.environ['LANGCHAIN_TRACING_V2'] = "true"
# os.environ['LANGCHAIN_PROJECT'] = "CRAG"
# os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"


OPENAI = os.environ["OPENAI_KEY"]
llm = ChatOpenAI(model='gpt-4.1',openai_api_key=OPENAI)


# def portfolio_loading(pdf_file:str):

#     doc = fitz.open(pdf_file)
#     for i, page in enumerate(doc):
#         img = page.get_pixmap()
#         img.save(f"{output_folder}/SALES_{i}.png")
#     doc.close()

def portfolio_an(pdf_file):
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



if __name__ == '__main__':

    portfolio_analysis('./pdf/CV.pdf')
