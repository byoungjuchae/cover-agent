from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
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
from fastapi import FastAPI, UploadFile, File, Form
import requests
import requests
import json
from CV_writing.CV_re import cv_write
from fastapi import FastAPI, File, UploadFile



app = FastAPI()

load_dotenv()


# os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
# os.environ['LANGCHAIN_TRACING_V2'] = "true"
# os.environ['LANGCHAIN_PROJECT'] = "CRAG"
# os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"


INSERT_TOKEN = os.getenv("INSERT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

class State(BaseModel):
    
    text : str
    input_pdf : str
    input_JD : str
    response_pdf : str
    response_JD : str
    result : str
    score : str
    
llm = ChatOpenAI(model="gpt-4.1-mini", openai_api_key=OPENAI_KEY,temperature=0.7)


def make_config():
    return {"configurable": {"thread_id": str(uuid.uuid4())}}

class JobSearchConfig(BaseModel):
    job: str
    start_day: str
    start_month: str
    start_year: str
    end_day: str
    end_month: str
    end_year: str



current_config = JobSearchConfig(
    job="AI%20Engineer",
    start_day="12",
    start_month="05",
    start_year="2025",
    end_day="13",
    end_month="05",
    end_year="2025"
)
start_index = 0

@app.post("/set_job_config")
def set_job_config(config: JobSearchConfig):
    global current_config
    current_config = config
    return {"message": "Job configuration updated successfully."}




@app.post('/job_posting')
def get_url():
    global start_index, current_config 
    headers = {
    'X-RestLi-Protocol-Version': '2.0.0',
    'Linkedin-Version': '202503',
    'Authorization': f'Bearer {INSERT_TOKEN}'  
    }


    url = f"https://api.linkedin.com/rest/jobLibrary?q=criteria&keyword={current_config.job}&dateRange=(start:(day:{current_config.start_day},month:{current_config.start_month},year:{current_config.start_year}),end:(day:{current_config.end_day},month:{current_config.end_month},year:{current_config.end_year}))&start={start_index}&count=5"
    
    response = requests.get(url,headers=headers)
 
    docs = []
    for i in range(len(response.json()['elements'])):
        name = os.path.basename(response.json()['elements'][i]['jobPostingUrl'])
        docs.append(response.json()['elements'][i])
    start_index += 1
    return docs


@app.post('/pdf')
async def pdf_load(pdf_file: UploadFile = File(...)):
    save_path = f"./uploaded_files/{pdf_file.filename}"

    # 디렉토리 없으면 생성
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 저장
    with open(save_path, "wb") as buffer:
        content = await pdf_file.read()  # 비동기 read
        buffer.write(content)

    return {"message": f"파일이 저장되었습니다: {save_path}"}

class OuterModel(BaseModel):
    request: str
    jobdes: str
    name : str
@app.post('/chat', description="Chat endpoint for cover letter AI agent")
async def chat(data:OuterModel):
    """
    사용자의 메시지를 받아 Cover Letter 에이전트를 실행합니다.
    """

    config = {"configurable": {"thread_id": "53"}}

    agents = create_react_agent(
        llm,
        tools=[coverwriter],
        prompt=(
            "You're a helpful assistant designed to use tools effectively. "
            "When a question comes in, don't ask for permission—just use the tool. "
            "If the user wants assistance crafting a cover letter, execute 'coverwriter'. "
            "If the user wants to find a specific company, execute 'RAG'. "
            "For complex tasks, break them down and use tools step by step."
        )
    )
    
    user_input = data.request + 'Here is the Job description:' + data.jobdes

    response_text = ""
    chunks = []
    async for chunk in agents.astream(
        {"messages": [("human", user_input)]},
        config=config
    ):  
        chunks.append(chunk)
        print(chunk)

    response_text += chunks[-2]['tools']['messages'][0].content
    return {"reply": response_text}



if __name__ == '__main__':
    files = {"request": "write a cover letter"}
                           
    asyncio.run(chat(files))
