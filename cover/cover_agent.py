from langgraph.graph import StateGraph, END

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import json
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import asyncio


mcp = FastMCP("coverwriter")

load_dotenv()
class State(BaseModel):
    
    text : str = Field(default='')
    input_pdf : str = Field(default='')
    input_JD : str = Field(default='')
    response_pdf : str = Field(default='')
    response_JD : str = Field(default='')
    result :str =  Field(default='')
    score :str= Field(default='')


OPENAI_KEY = os.getenv("OPENAI_KEY")
llm = ChatOpenAI(model='gpt-4.1-mini',openai_api_key = OPENAI_KEY,temperature=0.7)

class company_jd(BaseModel):
    job_description : str = Field(default='',description='this is the job description about the company.')



async def analyze_pdf(state: State):
    prompt_text = """ You are a applicant. 
    you have to analyze the resume for applicants.
    analyze resume based on the performance with metrics.
    
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
    write it based on my resume, highlighting the overlapping areas between the job description and my experience. Exclude anything that isn’t directly relevant or that I haven’t actively worked on. 
    You only respond the cover letter.
    
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

    prompt_text = """ you are an outstanding recruiter, assess whether the cover letter effectively showcases the key strengths from my resume that match the job description. 
    If needed, enhance those areas to ensure they are prominently emphasized based on assessment and emphasizes my strengths with the cover letter stratgey.

    You only respond the revised cover letter.
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


graph_state = StateGraph(State)

graph_state.add_node("analyze_JD",analyze_JD)
graph_state.add_node("analyze_pdf",analyze_pdf)
graph_state.add_node("writer_grade",writer_grade)
graph_state.add_node("checker",checker)
graph_state.add_node("writer",writer)


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

graph_state.set_entry_point("analyze_JD")
graph = graph_state.compile()
import pdb
pdb.set_trace()

@mcp.tool()
async def coverwriter(job_description:str):
    """if you want to help writing a cover letter, use this tool"""

    state = State()

    state.input_JD = job_description
  

    response = await graph.ainvoke(state)
    
    return response['result']

if __name__ == "__name__":
    print("coverwriter start")
    mcp.run(transport="stdio")
