import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="충청북도 분기별 날씨 현황", layout="wide")

st.title("🌤 충청북도 분기별 날씨 현황 대시보드")

FILE_NAME = "충청북도_분기별날씨현황.csv"

# --------------------------
# 1️⃣ CSV 자동 인코딩 감지
# --------------------------

def load_csv_safely(file_path):
    encodings = ["utf-8", "cp949", "euc-kr", "ansi"]
    for enc in encodings:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            return df, enc
        except:
            pass
    return None, None

df, enc_used = load_csv_safely(FILE_NAME)

if df is None:
    st.error(f"❌ CSV 파일을 찾을 수 없습니다.\n📁 같은 폴더에 `{FILE_NAME}` 를 넣어주세요.")
    st.stop()

st.success(f"📁 CSV 로딩 성공 (인코딩: **{enc_used}**)")

# --------------------------
# 2️⃣ 기간(구분) → 연도 / 분기 추출
# --------------------------

def extract_year_month(x):
    m = re.search(r"(\d{2})-(\d{2})", str(x))
    if m:
        return f"20{m.group(1)}-{m.group(2)}"
    return None

df["date"] = df["구분"].apply(extract_year_month)

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["quarter"] = df["date"].dt.to_period("Q").astype(str)

# --------------------------
# 3️⃣ 수치형 컬럼만 추출 후 분기별 평균
# --------------------------

numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()

quarterly = df.groupby("quarter")[numeric_cols].mean().round(2).reset_index()

st.subheader("📊 분기별 평균 요약 테이블")
st.dataframe(quarterly)

# --------------------------
# 4️⃣ 사이드바 인터페이스
# --------------------------

st.sidebar.header("⚙️ 설정")

selected_indicator = st.sidebar.selectbox(
    "📌 비교할 날씨 항목 선택",
    numeric_cols
)

show_n = st.sidebar.slider(
    "📅 최근 몇 개 분기 표시?",
    min_value=3, max_value=len(quarterly), value=6
)

# 최근 N분기만 남기기
plot_df = quarterly.tail(show_n)
