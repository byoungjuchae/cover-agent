from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import InMemorySaver
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
    score : str
    
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_KEY)
docs = PyPDFLoader('./pdf/CV.pdf').load()

# embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
with open('./jobposting/4192684412.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

docs = [doc.page_content for doc in docs]


####### analyze the pdf 

async def analyze_pdf(state: State):
    prompt_text = """ You are a applicant. 
    you have to analyze the resume for applicants.
    
    Here is the resume:
    {resume}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    chain = {"resume":RunnablePassthrough()} | prompt | llm | StrOutputParser()
    
    response = await chain.ainvoke({"resume":docs[0]})
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

async def writer_grade(state:State):

    prompt_text = """ As an outstanding recruiter, please review the draft of my cover letter and evaluate how well it aligns with the job description and my resume. 
    If there are any parts that do not match the JD or resume, feel free to remove them. Please focus on emphasizing my strengths and based on the resume's fact.

    Here is the cover letter:
    {cover_letter}

    Here is the job description:
    {job_description}


    Here is the resume:
    {resume}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    chain = {'cover_letter':RunnablePassthrough(),'job_description':RunnablePassthrough(),'resume':RunnablePassthrough()} | prompt | llm | StrOutputParser()

    response = await chain.ainvoke({"cover_letter":state.response_JD,"resume":state.response_pdf,"cover_letter":state.result})
    state.result = response
    return state

async def checker(state:State):

    prompt_text = """ you are a good helper to check the cover letter. What is the score of this cover letter among the 10?

    You only answer the number. 

    Here is the cover letter
    {cover_letter} 
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    chain = {'cover_letter':RunnablePassthrough()} | prompt | llm | StrOutputParser()
    response = await chain.ainvoke({"cover_letter":state.result})
    state.score = response
    return state

async def should_end(state:State):
  
    if int(state.score) < 7:
        return "write"

    else:
        return END
async def start(state: State):

    print("start")
    return state
graph_state = StateGraph(State)

graph_state.add_node("analyze_JD",analyze_JD)
graph_state.add_node("analyze_pdf",analyze_pdf)
graph_state.add_node("writer_grade",writer_grade)
graph_state.add_node("checker",checker)
graph_state.add_node("writer",writer)
graph_state.add_node("start",start)

graph_state.add_edge("start","analyze_JD")
graph_state.add_edge("analyze_JD","analyze_pdf")
graph_state.add_edge("analyze_pdf","writer")
graph_state.add_edge("writer","writer_grade")
graph_state.add_edge("writer_grade","checker")
graph_state.add_conditional_edges(
    "checker",
    path=should_end,
    path_map={
        "write": "writer_grade",
        END: END
    }

)
checkpointer = InMemorySaver()
graph_state.set_entry_point("start")

graph = graph_state.compile(checkpointer=checkpointer)
config = {"configurable":{"thread_id":"4"}}


async def token_generator():
    initial_state = {
    "text": "",
    "input_pdf": "",
    "input_JD": data['jobDetails']['jobDescription'],
    "response_pdf": "",
    "response_JD": "",
    "result": "",
    "score": ""
    }
    async for chunk in graph.astream(initial_state,config):
       
        yield chunk

async def main():
    async for chunk in token_generator():
        print("✅ Step result:", chunk)

asyncio.run(main())
