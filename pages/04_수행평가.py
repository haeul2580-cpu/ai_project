import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="충청북도 분기별 날씨", layout="wide")

DATA_FILE = "충청북도_분기별날씨현황_20250630 (1).csv"

# ---------------------------
# 1) 데이터 로드
# ---------------------------
@st.cache_data
def load_data():
    encodings = ["cp949", "utf-8", "euc-kr", "latin1"]
    for e in encodings:
        try:
            return pd.read_csv(DATA_FILE, encoding=e)
        except:
            pass
    # 최후 수단
    return pd.read_csv(DATA_FILE, encoding="utf-8", errors="replace")

df = load_data()
df.columns = df.columns.str.strip()

# ---------------------------
# 2) 컬럼 자동 감지
# ---------------------------
possible_region_cols = [
    c for c in df.columns 
    if any(k in c for k in ["동네","동","지역","시군구","시군","읍","면","구","시","구분","지역명"])
]

region_col = possible_region_cols[0] if possible_region_cols else None

if region_col is None:
    region_col = st.sidebar.selectbox("지역 컬럼을 선택하세요", df.columns.tolist())

numeric_cols = df.select_dtypes(include="number").columns.tolist()

if not numeric_cols:
    st.error("숫자형(분기별 수치) 컬럼이 없습니다. CSV를 다시 확인해주세요.")
    st.stop()

# ---------------------------
# 3) UI
# ---------------------------
st.title("🌦 충청북도 분기별 날씨 현황 대시보드")

st.sidebar.header("설정 패널")
st.sidebar.write(f"자동 감지된 지역 컬럼 → **{region_col}**")

category_cols = st.sidebar.multiselect(
    "표시할 분기/수치 컬럼 선택",
    options=numeric_cols,
    default=numeric_cols
)

regions = df[region_col].unique().tolist()
sel_region = st.selectbox("지역 선택", regions)

# ---------------------------
# 4) 비율 데이터 계산
# ---------------------------
grouped = df[[region_col] + category_cols].groupby(region_col).sum()
proportion = grouped.div(grouped.sum(axis=1), axis=0).fillna(0)

vals = proportion.loc[sel_region].sort_values(ascending=False)
cats = vals.index.tolist()
nums = vals.values.tolist()

# ---------------------------
# 5) 색상 (1등 빨강 + 파랑 그라데이션)
# ---------------------------
def color_scale(n):
    colors = []
    for i in range(n):
        if i == 0:
            colors.append("rgba(255,0,0,1)")
        else:
            alpha = max(0.12, 1 - i * 0.12)
            colors.append(f"rgba(0,0,255,{alpha})")
    return colors

colors = color_scale(len(nums))

# ---------------------------
# 6) Plotly 그래프
# ---------------------------
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=cats,
        y=nums,
        marker_color=colors,
        text=[f"{v:.1%}" for v in nums],
        textposition="auto",
    )
)

fig.update_layout(
    title=f"{sel_region} — 분기별 비율 그래프",
    xaxis_title="구분(분기)",
    yaxis_title="비율",
    yaxis_tickformat=".0%"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 7) 원본 데이터 보기
# ---------------------------
if st.checkbox("📄 원본 데이터 보기"):
    st.dataframe(df)

# ---------------------------
# 8) 비율 CSV 다운로드
# ---------------------------
if st.button("📥 비율 데이터 CSV 생성"):
    out = proportion.reset_index()
    export_name = "충청북도_분기별날씨_비율데이터.csv"
    out.to_csv(export_name, index=False, encoding="utf-8-sig")
    with open(export_name, "rb") as f:
        st.download_button("다운로드", f, file_name=export_name)



























