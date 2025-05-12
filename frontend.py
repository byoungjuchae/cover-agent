import streamlit as st
import requests

st.set_page_config(page_title="Cover Letter Chatbot", layout="centered")
st.title("🤖 Cover Letter Chatbot")

# JD & CV 저장
jd = st.text_area("📄 Job Description", height=150, key="jd")
cv_pdf = st.file_uploader("📎 Upload Your Resume (PDF)", type=["pdf"])

# 채팅 세션 관리
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask about your ATS matching...")

# 실제 Agent 호출 함수 (여기서 endpoint 연결)
def call_agent_api(jd, cv_pdf, question):
    url = "http://localhost:5002/cover_letter"  # 예시 endpoint
    payload = {
        "job_description": jd,
        "resume_text": cv_pdf,
        "question": question
    }
    try:
        response = requests.post(url, json=payload)
        return response.json().get("answer", "Sorry, I couldn't get a response.")
    except:
        return "🔌 Agent server not responding."

# 사용자 입력 처리
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    if jd and cv_pdf:
        reply = call_agent_api(jd, cv_pdf, user_input)
    else:
        reply = "⚠️ Please input both JD and Resume."

    st.session_state.chat_history.append(("agent", reply))
    with st.chat_message("assistant"):
        st.markdown(reply)

# 이전 대화 렌더링
for role, message in st.session_state.chat_history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(message)
