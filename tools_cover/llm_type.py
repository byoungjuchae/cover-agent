from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key = OPENAI_KEY,temperature=0.7)

client = MongoClient("mongodb://mongo:27017/")
db = client["mydb"]
collection = db["users"]