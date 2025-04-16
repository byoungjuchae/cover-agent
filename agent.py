from langgraph.graph import StateGraph, END
from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.text_splitters import RecursiveCharacterTextSplitter
import base64
from pydantic import BaseModel, Field
from pymilvus import MilvusClient


class State(BaseModel):
    
    text : str
    input_pdf : str
    input_JD : str
    response_pdf : str
    response_JD : str
    result : str
    
llm = ChatOllama(model='llama3.2:latest')
embedding = HuggingFaceEmbeddings(model='sentence-transformers/all-mpnet-base-v2')

docs = PyPDFLoader('ss').load()
jd_loader = WebBaseLoader("http://").load()

text_split = RecursiveCharacterTextSplitter(chunk_size=250,chunk_overlap=0)
doc = text_split.split_documents(docs) 
vectorstore = FAISS.from_documents(doc,embedding=embedding).as_retriever()
####### analyze the pdf 

async def analyze_pdf(state: State):
    prompt_text = """ You are a recruiter from tech company. 
    you have to analyze the resume.
    
    Here is the resume:
    {resume}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    chain = {"resume":RunnablePassthrough()} | prompt | llm | StrOutputParser()
    
    response = await chain.ainvoke({"resume":vectorstore})
    state.response = response
    return state

####### analyze the JD 
async def analyze_JD(state:State):
    prompt_text = """ You are a recruiter from tech company. 
    you have to analyze the JD.
    
    Here is the JD:
    {job_description}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    chain = {"job_description":RunnablePassthrough()} | prompt | llm | StrOutputParser()
    
    response = await chain.ainvoke({"job_description":jd})
    state.response = response
    return state

####### total analyzing the pdf and JD perspective of the recruiter

async def writer(state:State):
    prompt_text = """ You are a writer about the cover letter and you have a good expertise about the recruiter.
    You have to write the cover letter to refer the Job description and resume.
    
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
def start(state: State):
    
    print("start")
graph_state = StateGraph(State)

graph_state.add_node("analyze_JD",analyze_JD)
graph_state.add_node("analyze_pdf",analyze_pdf)
graph_state.add_node("writer",writer)
graph_state.add_node("start",start)

graph_state.add_edge("start","analyze_JD")
graph_state.add_edge("start","analyze_pdf")
graph_state.add_edge("analyze_JD","writer")
graph_state.add_edge("analyze_pdf","writer")

graph_state.set_entry_point("start")

graph = graph_state.compile()
 