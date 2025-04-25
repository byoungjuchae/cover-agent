import requests
from dotenv import load_dotenv
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field
import json


load_dotenv()
INSERT_TOKEN = os.getenv("INSERT_TOKEN")
# &countries=(value:List(urn%3Ali%3Acountry%3AUS))
#url = """https://api.linkedin.com/rest/jobLibrary?q=criteria&keyword='{job}'&dateRange=(start:(day:'{start_day}',month:'{start_month}',year:'{start_year}'),end:(day:'{end_day}',month:'{end_month}',year:'{end_year}'))&start=0&count='{count}'"""


GEMINI_KEY = os.getenv("GEMINI_KEY")


prompt_text = """ You are a good assistant. you have to respond the start_year, start_month, start_day, end_year, end_month,end_day, count and job to refer the instruction.
            
            if there is no data about start_year, start_month, start_day, end_year, end_month, end_day, count and job, please follow format.

            format
            'start_year: 2025, start_day: 1, start_month: 4, end_year: 2025, end_month: 4, end_day: 15, job='soft engineer'
            output format is json format.

            if there is space in job, please fill it %02.
            please use default start year 2025.
            Here is the instruction: 
            {instruction}

"""
prompt = ChatPromptTemplate.from_template(prompt_text)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_KEY)
chain = {'instruction':RunnablePassthrough()} | prompt | llm | JsonOutputParser()
response = chain.invoke({'instruction':"3월 3일 부터 3월 4일 까지 AI engineer 직종 추출해줘"})
headers = {
    'X-RestLi-Protocol-Version': '2.0.0',
    'Linkedin-Version': '202503',
    'Authorization': f'Bearer {INSERT_TOKEN}'  
}

# @tool
def get_url(response):

    job = response['job']
    start_day = response['start_day']
    start_month = response['start_month']
    start_year = response['start_year']
    end_day = response['end_day']
    end_month = response['end_month']
    end_year = response['end_year']

    url = f"https://api.linkedin.com/rest/jobLibrary?q=criteria&keyword={job}&dateRange=(start:(day:{start_day},month:{start_month},year:{start_year}),end:(day:{end_day},month:{end_month},year:{end_year}))&start=100&count=24"""
    response = requests.get(url,headers=headers)
 

    for i in range(len(response.json()['elements'])):
        name = os.path.basename(response.json()['elements'][i]['jobPostingUrl'])
        print(i)
        with open(f'./jobposting/{name}.json','w') as f:
            json.dump(response.json()['elements'][i],f,ensure_ascii=False,indent=4)


get_url(response)