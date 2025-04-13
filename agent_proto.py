from pydantic import BaseModel, Field
from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.vectorstores import FAISS
from pymilvus import MilvusClient
import requests

# client = MilvusClient('milvus_demo.db')


################################### First simple agent 
# docs = PyPDFLoader("./CV_ByungJoo.pdf").load()
# embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
# text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250,chunk_overlap=0)
# doc = text_splitter.split_documents(docs)
# vectorstore = FAISS.from_documents(doc,embedding=embedding).as_retriever()
# llm = ChatOllama(model='llama3.2:latest')

# prompt_text = """ You are a good job recruiter. you have to analyze the resume.
# and check the good points of the resume.

# Here is the resume:
# {resume}
# """
# import pdb
# pdb.set_trace()
# prompt = ChatPromptTemplate.from_template(prompt_text)
# chain = {"resume":vectorstore} | prompt | llm | StrOutputParser()
# print(chain.invoke("Analyze the resume."))




access_token = "AQUgWYB-PIkZy0dra4aYAHqSCF0npi7SojO-RT4rS4u9XJfaNum0gN9X3HLursVmMkckphvD5w-j11aYd9T9PfDOirzp944xMCFK8r9O1svCZnUqQCXx0lIYAx-rGe41SlWliYPUuFzl9uWdeKQO_uMX2bhuricFyQHuBQhSTD9_pPeRTbO6TSgYLeLxVeMj-ps5BDdxl-d3Mm3KhmrBHglst-_9UtCPnJnNtKGIeQiqq2hVvvnjUm71OGqTrqZMKXXEzEFxzwYPqd49AYWqs_AA7mRQrBdWzLmie_4QrsKB19PSUSP0PstffdhraPYk8Tlqa8TGUCkN7BUujdaj_cMiQWRV1A"

################################### url


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
# jd_docs = WebBaseLoader("https://www.linkedin.com/jobs/collections/recommended/").load()
# jd_doc = text_splitter.split_documents(jd_docs)
# vectorstore = FAISS.from_documents(jd_doc,embeddings=embedding).as_retriever()
# llm = ChatOllama(model='llama3.2:latest')

# prompt_text = """ You are a good job recruiter. you have to analyze the resume.
# and check the good points of the resume.

# Here is the resume:
# {resume}
# """
# prompt = ChatPromptTemplate.from_template(prompt_text)
# chain = {"resume":vectorstore} | prompt | llm | StrOutputParser()
# print(chain.invoke("Analyze the JD"))