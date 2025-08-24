from langgraph.prebuilt import create_react_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import tool
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from docx import Document
from .util.total_state import SuperState, WriteState
from operator import itemgetter
from .llm_type import llm,collection


                                    

@tool
async def rewrite_cv(id:str):
    """You can use this tool to rewrite the CV"""
    prompt_text = """ You are a writer about CV resume. you have to avoid the ATS with rewriting the CV.

                you have to rewrite the CV refer to the CV analysis and JD analysis. 
                CV analysis must have the keywords about the JD and maintain the base CV information and format.

                Here is the JD analysis:
                {JD_analysis}

                Here is the CV analysis:
                {resume_analysis} 
    """

    prompt = ChatPromptTemplate.from_template(prompt_text)
 
    chain = {"JD_analysis": itemgetter("JD_analysis") | RunnablePassthrough(),"resume": itemgetter("resume") | RunnablePassthrough()} | prompt | llm | StrOutputParser()


    response = await chain.ainvoke({'JD_analysis': JD_analysis,"resume": resume})

    return response         

@tool
async def write_coverletter(state:SuperState):
    "you have to write this tool, when you want to write cover letter. input is id"
    graph = graph_state.compile()
    state = State(id=id)
    response = await graph.ainvoke(state)
    
    return response

@tool
def save_docx(cover_letter:str,save_name:str):
    "If you want to save docx file, use this tool."
    doc = Document()
    doc.add_paragraph(cover_letter)
    doc.save(f"{save_name}.docx")
               
                                    
def Write_it_Latex(state:WriteState):

        prompt_text = """ You are a writer about CV resume. you have to avoid the ATS with rewriting the CV.

                You have to write it through the pylatex code.

                Here is the CV:
                {cv} 
                {CV} 
        """
        prompt = ChatPromptTemplate.from_template(prompt_text)

        chain = {"CV":RunnablePassthrough()} | prompt | llm | StrOutputParser()

        response = chain.invoke({"CV":state.cv_re})

        state.final_response = response
        return state

async def first_coverletter(state:WriteState):

    prompt_text = """ You are a writer about the cover letter and you have a good expertise about the recruiter.
    write it based on my resume, highlighting the overlapping areas between the job description and my experience. Exclude anything that isn’t directly relevant or that I haven’t actively worked on. 
    You only respond the cover letter.
    
    Here is the Job Description:
    {Job_Description}
    
    Here is the resume:
    {resume}

    """
    JD_analysis = collection.find_one({"_id": state['id']}, {"JD_analysis": 1, "_id": 0}).get("JD_analysis", "No JD analysis found")
    resume = collection.find_one({"_id": state['id']}, {"resume_analysis": 1,"_id":0}).get("resume_analysis", "No resume found")
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    chain = {"Job_Description": itemgetter("Job_Description") | RunnablePassthrough(),"resume" : itemgetter("resume") | RunnablePassthrough()} | prompt | llm | StrOutputParser()
    
    response = await chain.ainvoke({"Job_Description":JD_analysis,"resume":resume})
    
    collection.update_one({"_id": state['id']}, {"$set": {"cover_letter": response}},upsert=True)
    state['response'] = response
    
    
    return state
    
    
async def grader_coverletter(state:WriteState):

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
    
    cover_letter = state['response']
    job_description = collection.find_one({"_id": state['id']}, {"JD_analysis": 1, "_id": 0}).get("JD_analysis", "No JD analysis found")
    resume = collection.find_one({"_id": state['id']}, {"resume_analysis": 1, "_id": 0}).get("resume_analysis", "No resume found")

    prompt = ChatPromptTemplate.from_template(prompt_text)

    chain = {'cover_letter':RunnablePassthrough(),'job_description':RunnablePassthrough(),'resume':RunnablePassthrough()} | prompt | llm | StrOutputParser()

    response = await chain.ainvoke({"cover_letter":cover_letter,"resume":resume,"job_description":job_description})
    collection.update_one({"_id": state['id']}, {"$set": {"cover_letter": response}},upsert=True)
    state['result'] = response
    return state

graph_state = StateGraph(WriteState)
graph_state.add_node("writer_grade",grader_coverletter)
graph_state.add_node("writer",first_coverletter)
graph_state.add_edge("writer","writer_grade")
graph_state.set_entry_point("writer")        

