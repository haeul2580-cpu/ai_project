import streamlit as st

# 제목
st.title("💫 MBTI로 보는 찰떡 진로 추천!")

st.write("너의 MBTI를 골라봐! 🔮")
st.write("내가 너한테 딱 어울리는 진로 두 개를 추천해줄게 😎")

# MBTI 리스트
mbti_types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# 사용자 입력
user_mbti = st.selectbox("👉 MBTI 선택하기", mbti_types)

# MBTI별 진로 추천 데이터
career_dict = {
    "ISTJ": ["공무원 🧾", "회계사 💼"],
    "ISFJ": ["간호사 🏥", "교사 🍎"],
    "INFJ": ["상담사 💬", "작가 ✍️"],
    "INTJ": ["연구원 🔬", "전략가 ♟️"],
    "ISTP": ["기계공 🧰", "경찰 👮‍♂️"],
    "ISFP": ["디자이너 🎨", "요리사 👨‍🍳"],
    "INFP": ["심리상담가 💭", "작사가 🎵"],
    "INTP": ["프로그래머 💻", "교수 🎓"],
    "ESTP": ["마케터 📢", "기업가 💸"],
    "ESFP": ["배우 🎭", "유튜버 🎥"],
    "ENFP": ["기획자 📋", "작가 ✨"],
    "ENTP": ["창업가 🚀", "광고기획자 🎯"],
    "ESTJ": ["경영자 💼", "군인 🪖"],
    "ESFJ": ["교사 📚", "간호사 💉"],
    "ENFJ": ["강사 🎤", "상담가 💌"],
    "ENTJ": ["CEO 🏢", "정치가 🏛️"]
}

# 추천 결과 출력
if user_mbti:
    st.subheader(f"💡 {user_mbti} 유형에게 어울리는 진로는?")
    careers = career_dict[user_mbti]
    st.success(f"✨ {careers[0]} 그리고 {careers[1]} 어때? 😄")
    st.write("너의 성향에 딱 맞는 진로들이야! 🔥")

st.write("---")
st.caption("Made with ❤️ by ChatGPT-5")
