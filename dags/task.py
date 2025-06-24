from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator, get_current_context
from datetime import timedelta, datetime
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import requests

load_dotenv()
INSERT_TOKEN  = os.getenv("INSERT_TOKEN")

headers = {
'X-RestLi-Protocol-Version': '2.0.0',
'Linkedin-Version': '202503',
'Authorization': f'Bearer {INSERT_TOKEN}'  
}
class JobSearchConfig(BaseModel):
    job: str
    start_day: str
    start_month: str
    start_year: str
    end_day: str
    end_month: str
    end_year: str

current_config =JobSearchConfig(
    job="AI%20Engineer",
    start_day="12",
    start_month="05",
    start_year="2025",
    end_day="13",
    end_month="05",
    end_year="2025"
)
@task
def jobs_0():
    global current_config
    start_index = 0
    datas = []
    for start_index in range(500):

        url = f"https://api.linkedin.com/rest/jobLibrary?q=criteria&keyword={current_config.job}&dateRange=(start:(day:{current_config.start_day},month:{current_config.start_month},year:{current_config.start_year}),end:(day:{current_config.end_day},month:{current_config.end_month},year:{current_config.end_year}))&start={start_index}&count=5"
        response = requests.get(url,headers=headers)
    
        if response == 200:
            datas.append(response.json())

    return datas
            

@task
def jobs_500():
    global current_config
    start_index = 500
    datas = []

    for start_index in range(500,1000):

        url = f"https://api.linkedin.com/rest/jobLibrary?q=criteria&keyword={current_config.job}&dateRange=(start:(day:{current_config.start_day},month:{current_config.start_month},year:{current_config.start_year}),end:(day:{current_config.end_day},month:{current_config.end_month},year:{current_config.end_year}))&start={start_index}&count=5"
        response = requests.get(url,headers=headers)

        if response == 200:
            datas.append(response.json())

    return datas

@task
def transformation(task_id):

    context = get_current_context()
    data = context["ti"].xcom_pull(task_ids=task_id,key="return_value")




with DAG(
    dag_id ='job_crawling',
    schedule_interval = timedelta(days=1),
    start_date = datetime(2025,1,1),
    catchup=False
) as dag:


    crawling_job = jobs_0.override(task_id="crawling_jobs")()
    crawling_job500 = jobs_500.override(task_id="crawling_jobs500")()


    transform_job = transformation.override(task_id="transforms_jobs")('crawling_jobs')
    transform_job500 = transformation.override(task_id="transforms_jobs500")("crawling_jobs500")


    crawling_job >> transform_job
    
    crawling_job500 >> transform_job500
    


