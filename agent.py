from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
import sys
import os
from tools_.portfolio_analysis.porfolio import portfolio_analysi
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio
import os
import uuid
import streamlit as st
from tools_.cover.cover_agent import coverwriter
from tools_.make_docx.docx_save import save_docx
from fastapi import FastAPI, UploadFile, File, Request
from pydantic import BaseModel
import requests
import shutil
import json
from pymongo import MongoClient


app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")

db = client["mydb"]
users = db["users"]



load_dotenv()

LANGCHAIN_TRACING_V2 = 'false'
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
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

class JobSearchConfig(BaseModel):
    job: str
    start_day: str
    start_month: str
    start_year: str
    end_day: str
    end_month: str
    end_year: str
    
class OuterModel(BaseModel):
    request: str
    jobdes: str
    name : str



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
    start_index += 5
    return docs


@app.post('/CV_pdf')
async def CV_load(pdf_file: UploadFile = File(...)):
    UPLOAD_DIR = './uploaded_files_CV'
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    save_path = f"./uploaded_files_CV/{pdf_file.filename}"


    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    #### pdf 저장 in db
    with open(save_path, "wb") as buffer:
        content = await pdf_file.read()  
        buffer.write(content)

    return {"message": f"파일이 저장되었습니다: {save_path}"}

@app.post('/portfolio_pdf')
async def portfolio_load(pdf_file: UploadFile = File(...)):
    
    UPLOAD_DIR = './uploaded_files_portfolio'
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    save_path = f"./uploaded_files_portfolio/{pdf_file.filename}"


    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    #### pdf 저장 in db
    with open(save_path, "wb") as buffer:
        content = await pdf_file.read()  
        buffer.write(content)

    return {"message": f"파일이 저장되었습니다: {save_path}"}


llm = ChatOpenAI(model="gpt-4.1-mini", openai_api_key=OPENAI_KEY,temperature=0.7)
@app.post('/chat', description="Chat endpoint for cover letter AI agent")
async def chat(data:OuterModel):
    """
    사용자의 메시지를 받아 Cover Letter 에이전트를 실행합니다.
    """

    config = {"configurable": {"thread_id": "53"}}
    agents = create_react_agent(
        llm,
        tools=[coverwriter,portfolio_analysi,save_docx],
        prompt=(
            "You're a helpful assistant designed to use tools effectively. "
            "When a question comes in, don't ask for permission—just use the tool. "
            "If the user wants assistance crafting a cover letter, execute 'coverwriter'."
            "If the user adds the portfolio file, execute 'portfolio_analysis'."
            "If the user wants to save the cover letter as a docx file, execute 'save_docx'."
            "For complex tasks, break them down and use tools step by step."
            
        )
    )
    user_input = data['request'] +"JD : you are a expert in AI"

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
    files = {"request": "write a coverletter and save the file as docx name of cover_letter"}
                           

    asyncio.run(chat(files))
