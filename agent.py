from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio
import os
import uuid
import streamlit as st
from cover.cover_agent import coverwriter
from job_rag.job_rag_agent import RAG
from fastapi import FastAPI, UploadFile, File
import requests
import json



app = FastAPI()

load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "CRAG"
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"

GEMINI_KEY = os.getenv("GEMINI_KEY")
INSERT_TOKEN = os.getenv("INSERT_TOKEN")


class State(BaseModel):
    
    text : str
    input_pdf : str
    input_JD : str
    response_pdf : str
    response_JD : str
    result : str
    score : str
    
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_KEY)
docs = PyPDFLoader('./pdf/CV.pdf').load()

def make_config():
    return {"configurable": {"thread_id": str(uuid.uuid4())}}



@app.post('/job_posting')
def get_url():
    headers = {
    'X-RestLi-Protocol-Version': '2.0.0',
    'Linkedin-Version': '202503',
    'Authorization': f'Bearer {INSERT_TOKEN}'  
    }

    job = "AI%02Engineer"
    start_day = "12"
    start_month = "05"
    start_year = "2025"
    end_day = "13"
    end_month = "05"
    end_year = "2025"

    url = f"https://api.linkedin.com/rest/jobLibrary?q=criteria&keyword={job}&dateRange=(start:(day:{start_day},month:{start_month},year:{start_year}),end:(day:{end_day},month:{end_month},year:{end_year}))&start=100&count=5"""
    response = requests.get(url,headers=headers)
 
    docs = []
    for i in range(len(response.json()['elements'])):
        name = os.path.basename(response.json()['elements'][i]['jobPostingUrl'])
        print(i)
        docs.append(response.json()['elements'][i])
       
    return docs


@app.post('/pdf')
async def pdf_load(pdf_file: UploadFile = File(...)):
    contents = await pdf_file.read()
    docs = PyPDFLoader(contents).load()
    return {"message": "PDF 처리 완료", "num_pages": len(docs)}

@app.post('/chat')
async def chat():

    print("📄 Cover Letter Chatbot Ready — 'exit' 입력 시 종료")
    config = {"configurable": {"thread_id": "53"}}
    agents= create_react_agent(llm,tools=[coverwriter,RAG],
    prompt=("You're a helpful assistant designed to use tools effectively. When a question comes in, don't ask for permission—if it looks like a tool should be used, just go ahead and use it."
            "if you want assistance crafting your cover letter, execute coverwriter."
            "if you want to find specific company, execute RAG"
            "Based on user needs, proactively select the most appropriate tool or combination of tools. For complex tasks, you can break down the problem and use different tools step by step to solve it. After using each tool, clearly explain the execution results and suggest the next steps."    
        )
    )
    while True:
        user_input = input()
        if user_input.strip().lower() in ("exit", "quit"):
            print("Bot: Goodbye! 👋")
            break
        async for chunk in agents.astream(
            {"messages": [("human", user_input)]},
            config=config
        ):

            print("\nBot COVER LETTER:\n")
            print(chunk)

docs = [doc.page_content for doc in docs]



if __name__ == '__main__':

    asyncio.run(chat())
