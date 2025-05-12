from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio
import os
import uuid
import streamlit as st
from cover.cover_agent import coverwriter
from langchain_mcp_adapters.client import MultiServerMCPClient
from fastapi import FastAPI


app = FastAPI()


load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "CRAG"
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"

GEMINI_KEY = os.getenv("OPENAI_KEY")


class State(BaseModel):
    
    text : str
    input_pdf : str
    input_JD : str
    response_pdf : str
    response_JD : str
    result : str
    score : str
    
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=GEMINI_KEY)


def make_config():
    return {"configurable": {"thread_id": str(uuid.uuid4())}}


@app.post('/cover_letter')
async def chat():
    
    async with MultiServerMCPClient(
    {
        "made_docx": {
        "command": "python",
        "args" :["./cover/docx_command.py"],
        "transport":"stdio"
        },
        "coverwriter":{
            "command":"python",
            "args":["./cover/cover_agent.py"],
            "transport":"stdio"
        }
        
    }

    ) as client:
        memory = InMemorySaver()
        store = InMemoryStore()
        tools = client.get_tools()
        print("📄 Cover Letter Chatbot Ready — 'exit'")
        config = {"configurable": {"thread_id": "53"},"checkpointer":memory,"store":store}
        agents= create_react_agent(llm,tools,
        prompt=("You're a helpful assistant designed to use tools effectively."
                "if the user wants to write a cover letter, you must write the document into the docx file "
                "you create the file in the /home directory."
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


if __name__ == '__main__':

    asyncio.run(chat())
