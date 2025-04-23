from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio
import os
import uuid
import streamlit as st
from langmem import create_manage_memory_tool, create_search_memory_tool
from cover.cover_agent import coverwriter
from job_rag.job_rag_agent import RAG


load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "CRAG"
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"

GEMINI_KEY = os.getenv("GEMINI_KEY")


    
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_KEY)
docs = PyPDFLoader('./pdf/CV.pdf').load()

def make_config():
    return {"configurable": {"thread_id": str(uuid.uuid4())}}

async def chat():
    print("📄 Cover Letter Chatbot Ready — 'exit' 입력 시 종료")
    config = {"configurable": {"thread_id": "53"}}
    agents= create_react_agent(llm,tools=[coverwriter,RAG],
    prompt=("You're a helpful assistant designed to use tools effectively. When a question comes in, don't ask for permission—if it looks like a tool should be used, just go ahead and use it."
            "if you want assistance crafting your cover letter, execute coverwriter."
            "if you want to find specific company, execute RAG"
            "Based on user needs, proactively select the most appropriate tool or combination of tools. For complex tasks, you can break down the problem and use different tools step by step to solve it. After using each tool, clearly explain the execution results and suggest the next steps."    
        )
    )
    while True:
        user_input = input()
        if user_input.strip().lower() in ("exit", "quit"):
            print("Bot: Goodbye! 👋")
            break
        async for chunk in agents.astream(
            {"messages": [("human", user_input)]},
            config=config
        ):

            print("\nBot COVER LETTER:\n")
            print(chunk)





# async def main():
#     async for chunk in token_generator():
if __name__ == '__main__':

    asyncio.run(chat())