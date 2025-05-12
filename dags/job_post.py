from langchain_milvus import Milvus
from glob import glob
import json
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os
from uuid import uuid4
from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv



embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')

vectorstore = Milvus(
    embedding_function=embedding,
    connection_args={
        "uri": "./milvus_demo.db",
    },
    index_params={"index_type": "FLAT", "metric_type": "L2"},
    consistency_level="Strong",
    drop_old=True,  # set to True if seeking to drop the collection with that name if it exists
)
load_dotenv()
INSERT_TOKEN = 'AQWbjYSPMgfCyyb0W-hBbXXPfjSzrj-JRoIAAEUeMDk6EnuGf7HXjJTqB4LR0Ld34MSjYWiSSHqRRFtGjbx9gdT4bmnVXQcss6EjKW5JaKwAj8yM7A_TLr5wajmi0vzzCcy16o-no7u5k69WQMtal2MQqqhTxYWSw_YWjiTYgCn7keJzEVa7SHr4litbe-Bsy7_AvvFm-jterGqEJeE6pzzhzbMzlUfaTphlhyBHhP91tUY_zAFby_mI8I8STvVoeav7W0TXr-TMNv212gd-1VULdVBEGBJPrLQ_pUYgE39xXYHqnNFAz5WpQ4lo-Foz-RhDyak5k8M3nr_ziRh3I1C9TFgJbg'
@task
def get_url():

    headers = {
        'X-RestLi-Protocol-Version': '2.0.0',
        'Linkedin-Version': '202503',
        'Authorization': f'Bearer {INSERT_TOKEN}'  
    }
    job = 'ai%02engineer'
    
    today = datetime.today().date()
    st = today - timedelta(days=1)
    end_year = today.year
    end_month = today.month
    end_day = today.day
    page = 1
    start_day = st.day
    start_month = st.month
    start_year = st.year
    
    # job = response['job']
    # start_day = response['start_day']
    # start_month = response['start_month']
    # start_year = response['start_year']
    # end_day = response['end_day']
    # end_month = response['end_month']
    # end_year = response['end_year']
    for i in range(1,1000):
        url = f"https://api.linkedin.com/rest/jobLibrary?q=criteria&keyword={job}&dateRange=(start:(day:{start_day},month:{start_month},year:{start_year}),end:(day:{end_day},month:{end_month},year:{end_year}))&start={i}&count=24"""
        response = requests.get(url,headers=headers)

        os.makedirs('./jobposting',exist_ok=True)
        for i in range(len(response.json()['elements'])):
            name = os.path.basename(response.json()['elements'][i]['jobPostingUrl'])
            print(name)
            with open(f'./jobposting/{name}.json','w') as f:
                json.dump(response.json()['elements'][i],f,ensure_ascii=False,indent=4)
            
            
@task    
def job_post():
    jobpost = glob(os.path.join("./jobposting",'*.json'))
    documented = []
    for i in range(len(jobpost)):
        with open(jobpost[i],'r') as f:
            data = json.load(f)

        documented.append(Document(page_content=data['jobDetails']['jobDescription'],
        metadata={'jobtitle':data['jobDetails']['jobTitle'],'joblocation':data['jobDetails']['jobLocation']}))
   

    URI = "http://localhost:19530"


    uuids = [str(uuid4()) for _ in range(len(documented))]
    vectorstore.add_documents(documents=documented, ids=uuids)


with DAG(
    dag_id ="scheduler_crawling",
    schedule_interval=timedelta(days=1),  
    start_date=datetime(2024, 1, 1),
    catchup=False,  
    tags=['crawl2']
) as dag:
    
    parse_job = get_url.override(task_id="crawling_post")()
    task_job = job_post.override(task_id="transform_post")()
    
    parse_job >> task_job
    