import streamlit as st
import requests
import PyPDF2
import textwrap

st.set_page_config(layout="wide")


def fetch_data():
    url = "http://localhost:8000/job_posting" 
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()[:2]
    return []


if "data" not in st.session_state:
    st.session_state.data = []
if "responses" not in st.session_state:
    st.session_state.response = []

st.sidebar.header("Job Search")
st.sidebar.header("📎CV Upload")
uploaded_file = st.sidebar.file_uploader("PDF format CV upload", type=["pdf"])

if uploaded_file is not None:



    files = {"pdf_file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}

    response = requests.post("http://localhost:8000/CV_pdf", files=files)

    if response.ok:
        st.sidebar.success("Success!")
    else:
        st.sidebar.error("Server Error")
        
        
st.sidebar.header("📎Portfolio Upload")
uploaded_file = st.sidebar.file_uploader("PDF format Portfolio upload", type=["pdf"])

if uploaded_file is not None:


    files = {"pdf_file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}

    response = requests.post("http://localhost:8000/portfolio_pdf", files=files)

    if response.ok:
        st.sidebar.success("Success!")
    else:
        st.sidebar.error("Server Error")

if "messages" not in st.session_state:
    st.session_state.messages = []  # 채팅 메시지 저장
if st.sidebar.button("🔄 Data reload"):
    st.session_state.data = fetch_data()

    for item in st.session_state.data:
        
        job = item.get("jobDetails", {})
        job_post = textwrap.dedent(f"""\
        # {job.get('jobTitle', 'N/A')}

        - **Company:** {job.get('organizationName', 'N/A')}
        - **Location:** {job.get('jobLocation', 'N/A')}
        - **Description:** {job.get('jobDescription', 'N/A')}

        {job.get('jobLongDescription', '')}
        """).strip()
        st.session_state.messages.append({"role": "assistant", "content": job_post })


for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

        # 버튼 클릭 시 API
   
        if st.button("Click", key=f"button_{i}"):
            with st.spinner("Sending job description..."):
                try:
                    response = requests.post(
                        "http://localhost:8000/job_description_post",
                        json={"description": msg["content"]}
                    )

                    if response.status_code == 200:
                        st.success("✅ Job description sent successfully")
                    else:
                        st.error(f"❌ API Error {response.status_code}: {response.text}")

                except Exception as e:
                    st.error(f"❌ Exception: {str(e)}")
        

st.sidebar.header("🛠️ Setting")

with st.sidebar.form("job_config_form"):
    job = st.text_input("🔍 Keyword (Example: AI Engineer)", value="AI Engineer")
    start_day = st.text_input("Start Day", value="12")
    start_month = st.text_input("Start Month", value="05")
    start_year = st.text_input("Start Year", value="2025")
    end_day = st.text_input("End Day", value="13")
    end_month = st.text_input("End Month", value="05")
    end_year = st.text_input("End Year", value="2025")
    submitted = st.form_submit_button("✅ Setting Adaption")

    if submitted:
        config_data = {
            "job": job.replace(" ", "%20"),  # URL-safe encoding
            "start_day": start_day,
            "start_month": start_month,
            "start_year": start_year,
            "end_day": end_day,
            "end_month": end_month,
            "end_year": end_year
        }

        try:
            response = requests.post("http://localhost:8000/set_job_config", json=config_data)
            if response.ok:
                st.success("🔄 Setting is success")
            else:
                st.error(f"❌ Fail: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ Exception: {str(e)}")


def handle_body(body):
    return f"서버로 전송된 body 내용 (앞 100자):\n\n{body[:100]}..."



if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("Type your message..."):
    # 사용자 메시지 저장

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    if uploaded_file is None:
        st.warning("⚠️ 먼저 PDF 파일을 업로드하세요.")
    else:
        # API 요청 데이터
        files = {
            "request": prompt,
            "name": uploaded_file.name
        }

        try:
            response = requests.post("http://localhost:8000/chat", json=files)

            if response.status_code == 200:
                data = response.json()
                for name, value in data.items():
                    last_message = value["messages"][-1]
                    st.session_state.messages.append({"role": "assistant", "content": last_message['content']})
                    with st.chat_message("assistant"):
                        st.markdown(last_message['content'])
                        
            else:
                st.error(f"❌ Fail: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"❌ Exception: {str(e)}")

  
        
# if st.button("🔁 Data F5"):
#     st.session_state.data = fetch_data()

# col1, col2 = st.columns([2, 3])
# with col1:
#     st.subheader("🗂️ List")
#     j=0
#     for i, item in enumerate(st.session_state.data):
        
#         job = item.get("jobDetails", {})
#         with st.container(border=True):

#             st.markdown(f"### List {i + 1}")
#             st.markdown(f"**Organization:** {job.get('organizationName', 'N/A')}")
#             st.markdown(f"**Location:** {job.get('jobLocation', 'N/A')}")
#             st.markdown(f"**Job Title:** {job.get('jobTitle', 'N/A')}")
#             st.markdown("**Job Description:**")

#             st.markdown(job.get("jobDescription", "N/A"))

#             # 입력창과 버튼을 가로로 나란히 배치
#             col_input, col_button = st.columns([4, 1])
#             with col_input:
#                 user_input = st.text_input(
#                     f"입력 메시지 ({i+1})", 
#                     placeholder="ex) Write a cover letter for this job",
#                     key=f"user_input_{i+1}"
#                 )
#             with col_button:

#                 if st.button(f"▶️ Send", key=f"send_{i+1}"):
                  
#                     if uploaded_file is None:
#                         st.warning("⚠️ 먼저 PDF 파일을 업로드하세요.")
#                     else:
#                         # 파일이 있는 경우에만 API 호출
#                         files = {
#                             "request": user_input,
#                             "jobdes": job.get("jobDescription", "N/A"),
#                             "name": uploaded_file.name
#                         }
                   
#                         try:
#                             response = requests.post("http://localhost:8000/chat", json=files)
#                             if response.status_code == 200:

#                                 st.success("✅ 전송 성공!")
#                                 st.success("✅ Success!")

#                                 st.session_state.response = response.json()
        
#                             else:
#                                 st.error(f"❌ Fail: {response.status_code} - {response.text}")
#                         except Exception as e:
#                             st.error(f"❌ Exception: {str(e)}")


