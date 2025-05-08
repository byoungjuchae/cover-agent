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
    st.sidebar.success("이력서 업로드 완료 ✅")
    # PDF 파일에서 텍스트 추출
    reader = PyPDF2.PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()

    st.sidebar.subheader("📃 이력서 요약")
    st.sidebar.text_area("추출된 내용 (요약)", extracted_text[:1000], height=300)

# 응답 처리 함수
def handle_body(body):
    return f"서버로 전송된 body 내용 (앞 100자):\n\n{body[:100]}..."

# API 호출 함수
def fetch_data():
    url = "https://jsonplaceholder.typicode.com/posts"  # ← 실제 API 주소로 변경
    response = requests.get(url)
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
        with st.container():
            st.markdown(f"**항목 {i+1}**")
            st.markdown(item.get("body", "No body content")[:80] + "...")
            if st.button(f"▶️ 전송", key=f"send_{i}"):
                st.session_state.response = handle_body(item.get("body", ""))

with col2:
    st.subheader("📥 처리 결과 (Response)")
    if st.session_state.response:
        st.code(st.session_state.response, language="markdown")
    else:
        st.info("왼쪽에서 항목을 선택해 주세요.")


