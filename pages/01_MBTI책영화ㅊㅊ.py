import streamlit as st

st.set_page_config(page_title="MBTI 취향 저격 🎬📚", page_icon="🎭", layout="centered")

st.title("✨ MBTI로 알아보는 책 & 영화 추천 ✨")
st.write("자기 MBTI를 골라봐! 너한테 찰떡인 책이랑 영화 알려줄게 😆")

# MBTI 리스트
mbti_list = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 선택 박스
user_mbti = st.selectbox("👉 너의 MBTI는?", mbti_list)

# MBTI별 추천 데이터
recommendations = {
    "INTJ": {
        "books": [
            ("달러구트 꿈 백화점", "차분하고 사색적인 너에게 어울리는 따뜻한 판타지 💭"),
            ("아몬드", "감정의 본질을 탐구하는 이야기가 딱 너 스타일 😌")
        ],
        "movies": [
            ("인터스텔라", "논리와 철학이 동시에 녹아있는 SF 명작 🚀"),
            ("셜록 홈즈", "지적인 추리를 즐기는 INTJ에게 찰떡 🕵️‍♂️")
        ]
    },
    "INFP": {
        "books": [
            ("82년생 김지영", "공감력 만렙 INFP의 마음을 울릴 현실 이야기 💔"),
            ("죽은 시인의 사회", "이상과 자유를 사랑하는 너에게 딱이야 🌸")
        ],
        "movies": [
            ("라라랜드", "꿈과 사랑 사이에
