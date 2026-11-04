# 📋 app.py · [실습 1-4] session_state 로 고친 카운터 (요청 없음)
import streamlit as st

st.title("🔢 클릭 카운터 (session_state 버전)")

if "count" not in st.session_state:         # 이 탭에서 처음 실행될 때만
    st.session_state.count = 0              # 0 으로 만들어 둠 (다시 실행돼도 지워지지 않는 보관함)

if st.button("+1"):
    st.session_state.count = st.session_state.count + 1

if st.button("처음으로"):
    st.session_state.count = 0

st.metric("누른 횟수", st.session_state.count)
