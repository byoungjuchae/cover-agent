from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import base64
from pydantic import BaseModel, Field
from pymilvus import MilvusClient
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "CRAG"
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"

GEMINI_KEY = os.getenv("GEMINI_KEY")

class State(BaseModel):
    
    text : str
    input_pdf : str
    input_JD : str
    response_pdf : str
    response_JD : str
    result : str
    
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_KEY)

# embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
with open('./jobposting/4192684412.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


text_split = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250,chunk_overlap=0)
# doc = text_split.split_text(json_data=data,covert_lists=True) 
# document = [Document(
#     page_content = data['jobDetails']['jobDescription']
# )]
# vectorstore = FAISS.from_documents(document,embedding=embedding).as_retriever()

####### analyze the pdf 

async def analyze_pdf(state: State):
    prompt_text = """ You are a applicant. 
    you have to analyze the resume for applicants.
    
    Here is the resume:
    {resume}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    chain = {"resume":RunnablePassthrough()} | prompt | llm | StrOutputParser()
    
    response = await chain.ainvoke({"resume":vectorstore})
    state.response_pdf = response
    return state

####### analyze the JD 
# async def analyze_JD(state:State):
async def analyze_JD(state: State):
    prompt_text = """ You are are applicant. you have to apply the company.
    you have to analyze the JD and make a best strategy writing a cover letter for this company.
    
    Here is the JD:
    {job_description}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    chain = {"job_description":RunnablePassthrough()} | prompt | llm | StrOutputParser()
    
    response = await chain.ainvoke({"job_description":state.input_JD})
    state.response_JD = response
    return state
# print(analyze_JD(data['jobDetails']['jobDescription']))
####### total analyzing the pdf and JD perspective of the recruiter

async def writer(state:State):
    prompt_text = """ You are a writer about the cover letter and you have a good expertise about the recruiter.
    You have to write the cover letter to refer the Job Description and resume. Only respond the cover letter. 
    
    Here is the Job Description:
    {Job_Description}
    
    Here is the resume:
    {resume}

    """
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    chain = {"Job_Description":RunnablePassthrough(),"resume":RunnablePassthrough()} | prompt | llm | StrOutputParser()
    
    response = await chain.ainvoke({"Job_Description":state.response_JD,"resume":state.response_pdf})

    state.result =response
    return state
async def start(state: State):

    print("start")
    return state
graph_state = StateGraph(State)

graph_state.add_node("analyze_JD",analyze_JD)
graph_state.add_node("analyze_pdf",analyze_pdf)
graph_state.add_node("writer",writer)
graph_state.add_node("start",start)

graph_state.add_edge("start","analyze_JD")
#graph_state.add_edge("start","analyze_pdf")
graph_state.add_edge("analyze_JD","writer")
#graph_state.add_edge("analyze_pdf","writer")

graph_state.set_entry_point("start")

graph = graph_state.compile()


async def token_generator():
    initial_state = {
    "text": "",
    "input_pdf": "",
    "input_JD": data['jobDetails']['jobDescription'],
    "response_pdf": "",
    "response_JD": "",
    "result": ""
    }
    async for chunk in graph.astream(initial_state):
       
        yield chunk

async def main():
    async for chunk in token_generator():
        print("✅ Step result:", chunk)

asyncio.run(main())