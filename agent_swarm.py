from tools_cover.util.total_state import JobSearchConfig, JobDescriptionRequest, OuterModel, SwarmState
from tools_cover.swarm import graph_total as graph
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Request
from pymongo import MongoClient
import requests
import uuid
import os
import shutil
import asyncio

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

app = FastAPI()
client = MongoClient("mongodb://mongo:27017/")

db = client["mydb"]
collection = db["users"]

uuids = str(uuid.uuid4())
collection.insert_one(
    {"_id": uuids},
)


INSERT_TOKEN = "AQVxrzLAaAGKIAqGD-MnqbQknsNOzzgUQ5O8ssnSHi2XsUBV2LC4eIxyVbkKylI7CcqrVdTTJXQszw6PKi_QMwTuik3IK1QgXXvN8-megInTTVgvfAWRFrDKfEq2Kv7ZA9Vo4RTl8bnvXQJPy4uDAr0_94Rb9bbPwqYWmvPov8788uQ6bbWHNAFdXOTtUHY7CxPfmHPeRf1mnAn4-xUXBTFCtdTM_-VRBt6zn7EI6G_eQlE0HLvE8ZH4qJAoKPxn3QJi3UsywZLYPquRGvcqDRIHdfGTgDsVMNvbCgBHVoumjKfy-qHUQcO0sj1Mo4VSmdQHgazKeUzgOyovtnac4sv0PoWmjQ"



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



@app.post('/job_posting')
def get_url():
    global start_index, current_config 
    headers = {
    'X-RestLi-Protocol-Version': '2.0.0',
    'Linkedin-Version': '202506',
    'Authorization': f'Bearer {INSERT_TOKEN}'  
    }

    url = f"https://api.linkedin.com/rest/jobLibrary?q=criteria&keyword={current_config.job}&dateRange=(start:(day:{current_config.start_day},month:{current_config.start_month},year:{current_config.start_year}),end:(day:{current_config.end_day},month:{current_config.end_month},year:{current_config.end_year}))&start={start_index}&count=2"

    response = requests.get(url,headers=headers)

    docs = []

    for i in range(len(response.json()['elements'])):
        name = os.path.basename(response.json()['elements'][i]['jobPostingUrl'])
        docs.append(response.json()['elements'][i])
    start_index += 2
    return docs


@app.post("/set_job_config")
def set_job_config(config: JobSearchConfig):
    global current_config
    current_config = config
    return {"message": "Job configuration updated successfully."}


@app.post('/job_description_post')
def job_description(description: JobDescriptionRequest):
    
    collection.update_one(
        {"_id":uuids},
        {"$set":{"job_description":description.description}},
        upsert=True
    )
    
    
@app.post('/portfolio_pdf')
async def portfolio_load(pdf_file: UploadFile = File(...)):
    
    UPLOAD_DIR = './uploaded_files_portfolio'
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    save_path = f"./uploaded_files_portfolio/{pdf_file.filename}"

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(pdf_file.file, buffer)
    pdf_file.file.close()
    
    collection.update_one(
        {"_id": uuids},
        {"$set": {"portfolio": save_path}},
        upsert=True
    )


@app.post('/CV_pdf')
async def CV_load(pdf_file: UploadFile = File(...)):
    UPLOAD_DIR = './uploaded_files_CV'
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    save_path = f"./uploaded_files_CV/{pdf_file.filename}"


    os.makedirs(os.path.dirname(save_path), exist_ok=True)
  
    with open(save_path, "wb") as buffer:
       
        shutil.copyfileobj(pdf_file.file, buffer)
    pdf_file.file.close()
    
    collection.update_one(
        {"_id": uuids},
        {"$set": {"CV": save_path}},
        upsert=True
    )

@app.post('/chat', description="Chat endpoint for cover letter AI agent")
async def chat(data:OuterModel):

    config = {"configurable": {"thread_id": "25"}}
    messages = []
    state = SwarmState(id=uuids, messages=data.request, plan="", response="", result="")

    collection.update_one({"_id": uuids}, {"$set": {"user_input": data.request}}, upsert=True)
    async for message in graph.astream(state,config):

        messages.append(message)
  

    
    return messages[-1]


