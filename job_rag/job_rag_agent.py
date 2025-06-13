from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from glob import glob 
import os
import json
from uuid import uuid4




    

def job_post():
    jobpost = glob(os.path.join("./jobposting",'*.json'))
    documented = []
    for i in range(len(jobpost)):
        with open(jobpost[i],'r') as f:
            data = json.load(f)

        documented.append(Document(page_content=data['jobDetails']['jobDescription'],
        metadata={'jobtitle':data['jobDetails']['jobTitle'],'joblocation':data['jobDetails']['jobLocation']}))
    embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')


    URI = "http://localhost:19530"

    vectorstore = Milvus(
        embedding_function=embedding,
        connection_args={
            "uri": "./milvus_demo.db",
        },
        index_params={"index_type": "FLAT", "metric_type": "L2"},
        consistency_level="Strong",
        drop_old=True,  # set to True if seeking to drop the collection with that name if it exists
    )
    uuids = [str(uuid4()) for _ in range(len(documented))]
    vectorstore.add_documents(documents=documented, ids=uuids)
    return vectorstore

class Company(BaseModel):
    company_name: str


@tool(args_schema=Company)
async def RAG(company_name:str):
    """If you want to find the company and jd, use this tool"""
    vectorstore = job_post()
    retriever = vectorstore.as_retriever()
    response = retriever.get_relevant_documents(company_name)
    return response[0].page_content