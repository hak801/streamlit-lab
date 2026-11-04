# 📋 app.py · [실습 1-3] 버튼을 누를 때마다 1씩 늘리기 — 첫 번째 시도 (요청 없음)
import streamlit as st

st.title("🔢 클릭 카운터 (실패 버전)")

count = 0                                   # 숫자를 0 으로 시작
if st.button("+1"):
    count = count + 1                       # 누르면 1 늘림

st.metric("누른 횟수", count)
st.caption("버튼을 여러 번 눌러 보세요. 숫자가 계속 늘어나나요?")
