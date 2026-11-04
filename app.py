# 📋 app.py · [실습 2-1] AI 용어 설명기 ① — client 만들기 · 키 확인 (요청 없음)
import streamlit as st
from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.5-flash-lite"


# ---------- ① client 만들기 : 키는 st.secrets 에서 읽음 (코드에 적지 않음) ----------
@st.cache_resource                          # 처음 한 번만 만들고, 다시 실행될 때는 만들어 둔 것을 그대로 씀
def get_client():
    """Gemini client 를 만들어 돌려준다"""
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options=types.HttpOptions(
            timeout=120_000,                                   # 2분 안에 답이 없으면 멈춤
            retry_options=types.HttpRetryOptions(http_status_codes=[500, 503]),   # 429 는 말없이 기다리지 않게
        ),
    )


# ---------- 키가 있는지 먼저 확인 ----------
try:
    client = get_client()
except Exception:
    st.error("🔑 GEMINI_API_KEY 를 찾지 못했습니다 — Manage app → ⋮ → Settings → Secrets 칸을 확인하세요.")
    st.stop()                               # 여기서 화면 그리기를 멈춤

# ---------- 화면 ----------
st.title("📝 AI 용어 설명기")
st.success("🔑 키를 찾았습니다 — client 준비 완료 (아직 요청은 보내지 않음)")
