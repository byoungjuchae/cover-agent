import streamlit as st
import requests
import PyPDF2

st.set_page_config(layout="wide")
st.title("📨 항목 선택 → 응답 보기 + 📄 CV 업로드")

# 세션 상태 초기화
if "data" not in st.session_state:
    st.session_state.data = []
if "response" not in st.session_state:
    st.session_state.response = ""

# --- 📄 CV 업로드 ---
st.sidebar.header("📎 이력서 업로드")
uploaded_file = st.sidebar.file_uploader("PDF 형식 이력서 업로드", type=["pdf"])

if uploaded_file is not None:
    st.write("파일 이름:", uploaded_file.name)
    reader = PyPDF2.PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()

    st.sidebar.subheader("📃 이력서 요약")
    st.sidebar.text_area("추출된 내용 (요약)", extracted_text[:1000], height=300)

    files = {"pdf_file": (uploaded_file.name, uploaded_file, "application/pdf")}
    response = requests.post("http://localhost:8000/pdf", files=files)

    if response.ok:
        st.success("PDF 전송 성공!")
        st.json(response.json())
    else:
        st.error("서버 에러")

# 응답 처리 함수
def handle_body(body):
    return f"서버로 전송된 body 내용 (앞 100자):\n\n{body[:100]}..."

# API 호출 함수
def fetch_data():

    url = "http://localhost:8000/job_posting"  # ← 실제 API 주소로 변경
    response = requests.post(url)

    if response.status_code == 200:
        return response.json()[:5]
    return []

# 새로고침 버튼
if st.button("🔁 데이터 새로고침"):
    st.session_state.data = fetch_data()

# 첫 진입 시 데이터 불러오기
if not st.session_state.data:
    st.session_state.data = fetch_data()

# 레이아웃
col1, col2 = st.columns([2, 3])


with col1:
    st.subheader("🗂️ 항목 목록")

    for i, item in enumerate(st.session_state.data):
        job = item.get("jobDetails", {})
        with st.container(border=True):
            st.markdown(f"### 항목 {i + 1}")
            st.markdown(f"**회사명 (Organization):** {job.get('organizationName', 'N/A')}")
            st.markdown(f"**위치 (Location):** {job.get('jobLocation', 'N/A')}")
            st.markdown(f"**직무 제목 (Job Title):** {job.get('jobTitle', 'N/A')}")
            st.markdown("**직무 설명 (Job Description):**")
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
                if st.button(f"▶️ 전송", key=f"send_{i}"):
                    if not user_input.strip():
                        st.warning("⛔ 메시지를 입력하세요!")
                    else:
                        payload = {
                            "message": user_input,
                            "job": job
                        }
                        try:
                            response = requests.post("http://localhost:8000/chat", json=payload)
                            if response.status_code == 200:
                                st.success("✅ 전송 성공!")
                                st.json(response.json())
                            else:
                                st.error(f"❌ 실패: {response.status_code} - {response.text}")
                        except Exception as e:
                            st.error(f"❌ 예외 발생: {str(e)}")


with col2:
    

    st.subheader("📥 처리 결과 (Response)")
    if st.session_state.response:
        st.code(st.session_state.response, language="markdown")
    else:
        st.info("왼쪽에서 항목을 선택해 주세요.")


