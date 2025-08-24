from langchain.prompts import ChatPromptTemplate
from langchain.tools import tool
from .util.total_state import SuperState, SwarmState
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from .llm_type import llm, collection


@tool
async def analyze_resume(state :SwarmState):
    """if you want to analyze the resume or CV, use this tool, input is the id of the user"""
    
    prompt_text = """ You are a applicant. \n
    you have to analyze the resume for applicants. \n
    analyze resume based on the performance with metrics.
    
    Here is the resume:
    {resume}
    """

    user_data = collection.find_one({"_id":state['id']},{"CV":1,"_id":0}).get("CV")

    loader = PyPDFLoader(user_data)
    docs = loader.load()
    pdf_text = "\n".join(doc.page_content for doc in docs)

    prompt = ChatPromptTemplate.from_template(prompt_text)

    chain = {"resume":RunnablePassthrough()} | prompt | llm | StrOutputParser()
    response = await chain.ainvoke({"resume":pdf_text})

    collection.update_one({"_id": state['id']}, {"$set": {"resume_analysis": response}},upsert=True)

    return response


@tool
async def analyze_JD(state: SuperState):
    """if you want to analyze the JD, use this tool. input is the id of the user."""
    prompt_text = """ You are are applicant. you have to apply the company.
    you have to analyze the JD and make a best strategy writing a cover letter for this company.
    
    Here is the JD:
    {job_description}
    """
    
    job_description = collection.find_one({"_id": state['id']}, {"job_description": 1, "_id": 0}).get("job_description", "No job description found")

    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    chain = {"job_description":RunnablePassthrough()} | prompt | llm | StrOutputParser()
    
    response = await chain.ainvoke({"job_description": job_description})
    
    collection.update_one({"_id": state['id']}, {"$set": {"JD_analysis": response}},upsert=True)
    
    return response

@tool
async def analyze_portfolio(state :SuperState):
    """you have to use this tool when you have to analysis portfolio, input is the id"""
   
    pdf_file = collection.find_one({"_id": state['id']},{"portfolio":1,"_id":0}).get("portfolio", "No portfolio found")
    loader = PyPDFLoader(pdf_file)
    docs = loader.load()
 
    with open(pdf_file,"rb") as file:
        #reader = PyPDF2.PdfReader(file)
        file.seek(0)
        encoded = base64.b64encode(file.read()).decode("utf-8")

    prompt = """You are a recruiter. You have to analyze this pdf file about the portfolio for writing CV and resume.:"""

    message = {
        "role": "user",
        "content": [
            {
                "type":"text",
                "text":prompt,

            },
            {
                "type":"file",
                "source_type":"base64",
                "data":encoded,
                "mime_type":"application/pdf",

            }
        ]}
   
    chain =  llm | StrOutputParser()
    response = await chain.ainvoke([message])
    print(response)
    
    return response


