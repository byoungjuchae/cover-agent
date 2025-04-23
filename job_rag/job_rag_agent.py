from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain.vectorstores import 
from pymilvus import MilvusClient
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

class Company(BaseModel):
    company_name: str



@tool(args_schema=Company)
async def RAG(company_name:str):
    """If you want to find the company and jd, use this tool"""
    print(company_name)
    return "NVDA"