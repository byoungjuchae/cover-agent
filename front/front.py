import streamlit as st
import requests
import PyPDF2

st.set_page_config(layout="wide")
st.title("📨 Cover Letter")


if "data" not in st.session_state:
    st.session_state.data = []
if "responses" not in st.session_state:
    st.session_state.response = []

st.sidebar.header("📎CV Upload")
uploaded_file = st.sidebar.file_uploader("PDF format CV upload", type=["pdf"])

if uploaded_file is not None:
   
<<<<<<< HEAD
<<<<<<< HEAD
    st.write("파일 이름:", uploaded_file.name)
=======
    st.write("Filename:", uploaded_file.name)
>>>>>>> 5b1b31de8ac8f9f71f1163adc86918c19b8e48f4
=======
    st.write("Filename:", uploaded_file.name)
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
    reader = PyPDF2.PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()

<<<<<<< HEAD
<<<<<<< HEAD
    st.sidebar.subheader("📃CV Summarize")
    st.sidebar.text_area("Summarization", extracted_text[:1000], height=300)
=======
    st.sidebar.subheader("📃 이력서 요약")
    st.sidebar.text_area("추출된 내용 (요약)", extracted_text, height=300)
>>>>>>> main

<<<<<<< HEAD
    files = {"pdf_file": ("ecv.pdf", open("./pdf/CV.pdf", "rb"), "application/pdf")}
=======
    files = {"pdf_file": (extracted_text, "application/json")}
>>>>>>> 5c360d1 (commit)
=======
    st.sidebar.subheader("📃CV Summarize")
    st.sidebar.text_area("Summarization", extracted_text[:1000], height=300)

    files = {"pdf_file": (uploaded_file.name, uploaded_file, "application/pdf")}
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
    response = requests.post("http://localhost:8000/pdf", files=files)

    if response.ok:
        st.success("Success!")
        st.json(response.json())
    else:
        st.error("Server Error")


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

<<<<<<< HEAD
<<<<<<< HEAD

st.sidebar.header("🛠️ 검색 기준 설정")

with st.sidebar.form("job_config_form"):
    job = st.text_input("🔍 검색 키워드 (예: AI Engineer)", value="AI Engineer")
    start_day = st.text_input("시작일(day)", value="12")
    start_month = st.text_input("시작월(month)", value="05")
    start_year = st.text_input("시작년(year)", value="2025")
    end_day = st.text_input("종료일(day)", value="13")
    end_month = st.text_input("종료월(month)", value="05")
    end_year = st.text_input("종료년(year)", value="2025")
    submitted = st.form_submit_button("✅ 설정 적용")

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
                st.success("🔄 설정이 성공적으로 적용되었습니다.")
            else:
                st.error(f"❌ 실패: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ 예외 발생: {str(e)}")
# 응답 처리 함수
=======
>>>>>>> 5b1b31de8ac8f9f71f1163adc86918c19b8e48f4
=======
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
def handle_body(body):
    return f"서버로 전송된 body 내용 (앞 100자):\n\n{body[:100]}..."


def fetch_data():
    url = "http://localhost:8000/job_posting" 
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()[:5]
    return []


if st.button("🔁 Data F5"):
    st.session_state.data = fetch_data()


if not st.session_state.data:
    st.session_state.data = fetch_data()


col1, col2 = st.columns([2, 3])


with col1:
    st.subheader("🗂️ List")

    for i, item in enumerate(st.session_state.data):
        job = item.get("jobDetails", {})
        with st.container(border=True):
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
            st.markdown(f"### List {i + 1}")
            st.markdown(f"**Organization:** {job.get('organizationName', 'N/A')}")
            st.markdown(f"**Location:** {job.get('jobLocation', 'N/A')}")
            st.markdown(f"**Job Title:** {job.get('jobTitle', 'N/A')}")
            st.markdown("**Job Description:**")
<<<<<<< HEAD
=======
            st.markdown(f"### 항목 {i + 1}")
            st.markdown(f"**회사명 (Organization):** {job.get('organizationName', 'N/A')}")
            st.markdown(f"**위치 (Location):** {job.get('jobLocation', 'N/A')}")
            st.markdown(f"**직무 제목 (Job Title):** {job.get('jobTitle', 'N/A')}")
            st.markdown("**직무 설명 (Job Description):**")
>>>>>>> main
=======
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
            st.markdown(job.get("jobDescription", "N/A"))

            # 입력창과 버튼을 가로로 나란히 배치
            col_input, col_button = st.columns([4, 1])
            with col_input:
                user_input = st.text_input(
                    f"입력 메시지 ({i+1})", 
                    placeholder="ex) Write a cover letter for this job",
                    key=f"user_input_{i}"
                )
            with col_button:
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
                if st.button(f"▶️ Send", key=f"send_{i}"):
                    if not user_input.strip():
                        st.warning("⛔ 메시지를 입력하세요!")
                    else:
                        files = {
                            "request": user_input,
                            "jobdes": job.get("jobDescription", "N/A"),
                            "name": uploaded_file.name
                            }
                   
                        try:
                            response = requests.post("http://localhost:8000/chat", json=files)
                            if response.status_code == 200:
<<<<<<< HEAD
<<<<<<< HEAD
                                st.success("✅ 전송 성공!")
=======
                                st.success("✅ Success!")
>>>>>>> 5b1b31de8ac8f9f71f1163adc86918c19b8e48f4
=======
                                st.success("✅ Success!")
>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
                                st.session_state.response = response.json()
        
                            else:
                                st.error(f"❌ Fail: {response.status_code} - {response.text}")
                        except Exception as e:
                            st.error(f"❌ Exception: {str(e)}")



<<<<<<< HEAD
=======
                if st.button(f"▶️ 전송", key=f"send_{i}"):
                    if not user_input.strip():
                        st.warning("⛔ 메시지를 입력하세요!")
                    else:
                        payload = {
                            "message": user_input
                        }
                        try:
                            headers = {"Content-Type": "application/json"}
                            response = requests.post("http://localhost:8000/chatas", json=payload)
                            if response.status_code == 200:
                                st.success("✅ 전송 성공!")
                                st.json(response.json())
                            else:
                                st.error(f"❌ 실패: {response.status_code} - {response.text}")
                        except Exception as e:
                            st.error(f"❌ 예외 발생: {str(e)}")
            
>>>>>>> main

with col2:
<<<<<<< HEAD
    st.subheader("📥 처리 결과 (Response)")
    # response가 있을 경우에만 출력
=======
    st.subheader("📥 Cover Letter Result")

>>>>>>> 5b1b31de8ac8f9f71f1163adc86918c19b8e48f4
=======
with col2:
    st.subheader("📥 Cover Letter Result")

>>>>>>> 10602bec9b75ad2bdac436d91b87816b395cc6a1
   
    if st.session_state.response:

        st.markdown(st.session_state.response['reply'])



