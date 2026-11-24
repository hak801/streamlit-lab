# app.py · 나만의 요리 레시피 도우미 화면
# Secrets: API_URL · APP_ACCESS_CODE

import base64
import io
import os

import requests
import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError


MAX_SIDE = 1024

# 예시 사진을 사용하려면 이 이름으로 사진을 저장하세요.
EXAMPLE_IMAGE = "example.jpg"


st.set_page_config(
    page_title="나만의 요리 레시피 도우미",
    page_icon="🍳",
)


# Streamlit Secrets에서 API 주소 읽기
try:
    API_URL = str(st.secrets["API_URL"]).rstrip("/")
except (KeyError, FileNotFoundError):
    # Colab에서 시험할 때 사용하는 주소
    API_URL = "http://localhost:8000"


# Streamlit Secrets에서 접근 코드 읽기
try:
    ACCESS_CODE = st.secrets["APP_ACCESS_CODE"]
except (KeyError, FileNotFoundError):
    ACCESS_CODE = ""


st.title("🍳 나만의 요리 레시피 도우미")

st.write(
    "만들고 싶은 음식 이름과 음식 또는 재료 사진을 올려 주세요."
)

st.caption(
    "사진만으로 식품의 신선도나 안전 여부를 판단할 수 없습니다."
)


def photo_b64(raw):
    """사진의 크기를 줄이고 JPEG와 base64로 변환합니다."""
    with Image.open(io.BytesIO(raw)) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image.thumbnail((MAX_SIDE, MAX_SIDE))

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)

    return base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")


def analyze(raw, food_name):
    """사진과 음식 이름을 API에 보내고 결과를 보여줍니다."""

    # 사진 변환
    try:
        image_data = photo_b64(raw)
    except (OSError, ValueError, UnidentifiedImageError):
        st.error(
            "사진을 읽을 수 없습니다. 다른 이미지 파일을 선택해 주세요."
        )
        return

    # 백엔드에 요청 보내기
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            json={
                "image_b64": image_data,
                "food_name": food_name,
            },
            headers={
                "X-Access-Code": ACCESS_CODE,
            },
            timeout=120,
        )
    except requests.RequestException:
        st.error(
            "API 서버에 연결하지 못했습니다. "
            "API_URL과 서버 상태를 확인해 주세요."
        )
        return

    # 서버 오류 처리
    if response.status_code != 200:
        try:
            detail = response.json().get(
                "detail",
                "오류 내용을 확인할 수 없습니다.",
            )
        except (ValueError, AttributeError):
            detail = response.text[:200]

        st.error(
            f"상태 번호 {response.status_code}: {detail}"
        )
        return

    # 서버 응답 확인
    try:
        data = response.json()
        result = data["result"]

        if not isinstance(result, dict):
            raise ValueError("결과 형식이 올바르지 않습니다")

    except (ValueError, KeyError, TypeError):
        st.error("서버의 응답 형식이 올바르지 않습니다.")
        return

    # 결과 표 표시
    st.subheader("레시피 결과")

    st.table(
        [
            {"항목": name, "내용": value}
            for name, value in result.items()
        ]
    )

    st.caption(
        f"상태 번호 200 · 토큰 {data.get('tokens', '확인 불가')}"
    )


# 음식 이름 입력
food_name = st.text_input(
    "만들고 싶은 음식 이름",
    max_chars=100,
    placeholder="예: 김치볶음밥",
)


# 카메라 또는 파일 업로드
camera = (
    st.camera_input("카메라로 찍기")
    if st.toggle("카메라 켜기")
    else None
)

upload = st.file_uploader(
    "또는 사진 파일 올리기",
    type=["png", "jpg", "jpeg", "webp"],
)

photo = camera or upload

if photo is not None:
    st.image(photo, width=240)


# 사용자가 올린 사진으로 분석
if st.button(
    "레시피 알아보기",
    key="go",
    disabled=photo is None or not food_name.strip(),
):
    with st.spinner("레시피를 알아보는 중입니다..."):
        analyze(
            photo.getvalue(),
            food_name.strip(),
        )


# example.jpg가 있으면 예시 사진 버튼 표시
if os.path.exists(EXAMPLE_IMAGE):
    if st.button(
        "예시 사진으로 해 보기",
        key="sample",
        disabled=not food_name.strip(),
    ):
        with open(EXAMPLE_IMAGE, "rb") as file:
            example_bytes = file.read()

        st.image(
            example_bytes,
            width=240,
        )

        with st.spinner("레시피를 알아보는 중입니다..."):
            analyze(
                example_bytes,
                food_name.strip(),
            )
