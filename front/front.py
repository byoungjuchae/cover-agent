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
   
    st.write("Filename:", uploaded_file.name)
    reader = PyPDF2.PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()

    st.sidebar.subheader("📃CV Summarize")
    st.sidebar.text_area("Summarization", extracted_text[:1000], height=300)

    files = {"pdf_file": (uploaded_file.name, uploaded_file, "application/pdf")}
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
            st.markdown(f"### List {i + 1}")
            st.markdown(f"**Organization:** {job.get('organizationName', 'N/A')}")
            st.markdown(f"**Location:** {job.get('jobLocation', 'N/A')}")
            st.markdown(f"**Job Title:** {job.get('jobTitle', 'N/A')}")
            st.markdown("**Job Description:**")
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
                                st.success("✅ Success!")
                                st.session_state.response = response.json()
        
                            else:
                                st.error(f"❌ Fail: {response.status_code} - {response.text}")
                        except Exception as e:
                            st.error(f"❌ Exception: {str(e)}")



with col2:
    st.subheader("📥 Cover Letter Result")

   
    if st.session_state.response:

        st.markdown(st.session_state.response['reply'])



