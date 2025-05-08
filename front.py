import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("📨 항목 선택 → 응답 보기")


if "data" not in st.session_state:
    st.session_state.data = []
if "response" not in st.session_state:
    st.session_state.response = ""

def handle_body(body):

    return f"서버로 전송된 body 내용 (앞 100자):\n\n{body[:100]}..."


def fetch_data():
    url = "https://jsonplaceholder.typicode.com/posts"  # ← 실제 API 주소로 변경
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[:5]
    return []


if st.button("🔁 데이터 새로고침"):
    st.session_state.data = fetch_data()


if not st.session_state.data:
    st.session_state.data = fetch_data()


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



