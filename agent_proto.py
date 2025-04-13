from pydantic import BaseModel, Field
from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.vectorstores import FAISS
from langgraph.graph import StateGraph
from pymilvus import MilvusClient
import requests
from dotenv import load_dotenv
import os

load_dotenv()
access_token = os.getenv("ACCESS_TOKEN")
# client = MilvusClient('milvus_demo.db')


################################### First simple agent 

docs = PyPDFLoader("./CV_ByungJoo.pdf").load()
embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250,chunk_overlap=0)
doc = text_splitter.split_documents(docs)
vectorstore = FAISS.from_documents(doc,embedding=embedding).as_retriever()
llm = ChatOllama(model='llama3.2:latest')




<<<<<<< HEAD
class State(BaseModel):
    
    JD_job : str
    JD_country : str
    resume_url : str
    resume_analysis: str
    JD_anaylsis: str
    
    
def analyze_resume(state:State):
    prompt_text = """ You are a good job recruiter. you have to analyze the resume.
    and check the good points of the resume.

    Here is the resume:
    {resume}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)
    chain = {"resume":vectorstore} | prompt | llm | StrOutputParser()
    response = chain.invoke("Analyze the resume.")
    state.resume_analysis = response
    return state

################################### url
def analyze_JD(state:State):
    url = "https://www.linkedin.com/job-library/job/detail/123456789"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Connection": "Keep-Alive",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        data = response.json()
        print("LinkedIn profile information:")
        print(data)
    else:
        print("API error:")
        print("status:", response.status_code)
        print("message:", response.text)
    jd_docs=""
    jd_doc = text_splitter.split_documents(jd_docs)
    vectorstore = FAISS.from_documents(jd_doc,embeddings=embedding).as_retriever()
    llm = ChatOllama(model='llama3.2:latest')

    prompt_text = """ You are a good job recruiter. you have to analyze the resume.
    and check the good points of the resume.

    Here is the resume:
    {resume}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)
    chain = {"resume":vectorstore} | prompt | llm | StrOutputParser()
    print(chain.invoke("Analyze the JD"))


#####################################  write cover letter
def write_cover(state:State):
    promp_text = """You are a good writer and Job recruiter. You refer the context of JD analysis and resume analysis.
    and you write the cover letter to apply the Job of the JD.
    
    Here is the JD analysis:
    {JD_anaylsis}
    
    Here is the resume analysis:
    {resume_analysis}
    
    """
    prompt = ChatPromptTemplate.from_template(promp_text)
    chain = {"JD_analysis": RunnablePassthrough(), "resume_analysis":RunnablePassthrough()} | prompt | llm | StrOutputParser()
    response = chain.invoke({"JD_analysis":{},"resume_analysis":{}})
    
    
def start_node(state:State):
    
    print("start")
    return state
    
graph = StateGraph(State)

graph.add_node("analyze_resume",analyze_resume)
graph.add_node("analyze_JD",analyze_JD)
graph.add_node("write_cover",write_cover)
graph.add_node("start_node",start_node)

<<<<<<< HEAD
graph.set_entry_point("start_node")

graph.add_edge("start_node","analyze_resume")
graph.add_edge("start_node","analyze_JD")
graph.add_edge("analyze_resume","write_cover")
graph.add_edge("analyze_JD","write_cover")

grap = graph.compile()
      
=======
# Here is the resume:
# {resume}
# """
# prompt = ChatPromptTemplate.from_template(prompt_text)
# chain = {"resume":vectorstore} | prompt | llm | StrOutputParser()
# print(chain.invoke("Analyze the JD"))
>>>>>>> 8abe9a14d6012e3bf0ee0f7b98dd639030da38df
