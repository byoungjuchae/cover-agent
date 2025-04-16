import requests
from dotenv import load_dotenv
import os 
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

INSERT_TOKEN = os.getenv("INSERT_TOKEN")
url = f"""https://api.linkedin.com/rest/jobLibrary?q=criteria&keyword='{job}'&countries=(value:List(urn%3Ali%3Acountry%3AUS))&dateRange=(start:(day:'{start_day}',month:'{start_month}',year:'{start_year}'),end:(day:'{end_day}',month:'{end_month}',year:'{end_year}'))&start=0&count='{count}'"""


GEMINI_KEY = os.getenv("GEMINI_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_KEY)
headers = {
    'X-RestLi-Protocol-Version': '2.0.0',
    'Linkedin-Version': '202503',
    'Authorization': f'Bearer {INSERT_TOKEN}'  
}
response = requests.get(url,headers=headers)
import pdb
pdb.set_trace()