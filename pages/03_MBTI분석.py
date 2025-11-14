# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple

st.set_page_config(page_title="Country MBTI Viewer", layout="wide")

MBTI_TYPES = [
    "INFJ","ISFJ","INTP","ISFP","ENTP","INFP","ENTJ","ISTP",
    "INTJ","ESFP","ESTJ","ENFP","ESTP","ISTJ","ESFJ","ESTP"  # note: if CSV order differs, we read from file
]

def hex_to_rgb(h: str) -> Tuple[int,int,int]:
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: Tuple[int,int,int]) -> str:
    return '#{:02x}{:02x}{:02x}'.format(*[max(0,min(255,int(x))) for x in rgb])

def interp_color(c1: str, c2: str, t: float) -> str:
    r1,g1,b1 = hex_to_rgb(c1)
    r2,g2,b2 = hex_to_rgb(c2)
    r = r1 + (r2-r1)*t
    g = g1 + (g2-g1)*t
    b = b1 + (b2-b1)*t
    return rgb_to_hex((r,g,b))

def generate_colors(n_remaining: int) -> List[str]:
    """
    Generate a list of n_remaining colors forming a gradient from deep blue to light blue.
    The caller should prepend the red color for rank 1.
    """
    if n_remaining <= 0:
        return []
    deep_blue = "#08306b"   # deep blue (for 2nd place)
    light_blue = "#c6dbef"  # light blue (for last)
    if n_remaining == 1:
        return [deep_blue]
    t_values = np.linspace(0, 1, n_remaining)
    return [interp_color(deep_blue, light_blue, t) for t in t_values]

# Title
st.title("🌍 Country MBTI 비율 뷰어 (Plotly + Streamlit)")
st.markdown("국가를 선택하면 해당 국가의 16개 MBTI 유형 비율을 인터랙티브한 막대그래프로 보여줍니다.")

# --- Data load: try local default filename, otherwise let user upload ---
DEFAULT_FILENAMES = [
    "countriesMBTI_16types (2).csv",
    "countriesMBTI_16types.csv",
    "countriesMBTI_16types.csv".replace(" ", "_")
]

df = None
for fn in DEFAULT_FILENAMES:
    try:
        df = pd.read_csv(fn)
        st.info(f"로컬 파일에서 데이터를 불러왔습니다: `{fn}`")
        break
    except Exception:
        df = None

if df is None:
    uploaded = st.file_uploader("CSV 파일 업로드 (첫 열: Country, 나머지 열: MBTI 타입별 비율)", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        st.success("파일 업로드 완료.")
    else:
        st.warning("로컬에 기본 파일이 없고 업로드도 하지 않았습니다. 위에서 CSV를 업로드해 주세요.")
        st.stop()

# Standardize: ensure first column is 'Country' (case-insensitive)
cols = df.columns.tolist()
# if first col not name 'Country', try to detect
if cols[0].lower() != "country":
    possible_country = None
    for c in cols:
        if c.lower() == "country":
            possible_country = c
            break
    if possible_country:
        df = df.rename(columns={possible_country: "Country"})
    else:
        # assume first column is country
        df = df.rename(columns={cols[0]: "Country"})

# MBTI columns: everything except Country
mbti_cols = [c for c in df.columns if c != "Country"]
# If there are stray whitespace names, strip them
mbti_cols = [c.strip() for c in mbti_cols]
df.columns = ["Country"] + mbti_cols

# convert MBTI columns to numeric (coerce)
for c in mbti_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# Sidebar controls
st.sidebar.header("설정")
country_list = sorted(df["Country"].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("국가 선택", country_list, index=0)
show_values = st.sidebar.checkbox("값(%) 라벨 표시", value=True)
normalize_hint = st.sidebar.checkbox("값을 0-100 (%)로 변환하여 표시 (원래가 소수인 경우)", value=True)

# Get data for selected country
row = df[df["Country"] == selected_country]
if row.empty:
    st.error("선택한 국가 데이터가 없습니다.")
    st.stop()

row = row.iloc[0]
values = row[mbti_cols].copy()

# If NaNs present, warn
if values.isnull().any():
    st.warning("몇몇 MBTI 값이 누락되어 있습니다(결측치). 그래프에서 NaN은 0으로 처리됩니다).")
values = values.fillna(0.0)

# If normalize_hint: detect whether sum ~1, if yes convert to percent
sum_vals = values.sum()
if normalize_hint:
    if 0.9 <= sum_vals <= 1.1:
        values = values * 100
    elif 0.9*100 <= sum_vals <= 1.1*100:
        # already percent-ish
        pass
    else:
        # leave as-is but still multiply if they look like fractions (<2)
        if sum_vals <= 2:
            values = values * 100

# Sort by value descending
vals_sorted = values.sort_values(ascending=False)
labels = vals_sorted.index.tolist()
yvals = vals_sorted.values.tolist()

# Colors: first = red, rest = blue gradient from deep to light
first_color = "#e41a1c"
n_rest = len(yvals) - 1
rest_colors = generate_colors(n_rest)
colors = [first_color] + rest_colors

# Build Plotly bar
fig = go.Figure()
fig.add_trace(go.Bar(
    x=labels,
    y=yvals,
    marker_color=colors,
    text=[f"{v:.2f}%" if normalize_hint else f"{v:.2f}" for v in yvals] if show_values else None,
    textposition="auto" if show_values else None,
    hovertemplate="%{x}: %{y:.2f}%<extra></extra>" if normalize_hint else "%{x}: %{y}<extra></extra>"
))

fig.update_layout(
    title=f"{selected_country} — MBTI 분포",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)" if normalize_hint else "값",
    template="simple_white",
    margin=dict(l=40, r=20, t=80, b=40),
    yaxis=dict(tickformat=".1f")
)

st.plotly_chart(fig, use_container_width=True, theme="streamlit")

# Show raw row if user wants
with st.expander("원본 행 데이터 보기"):
    st.write(row.to_frame(name="Value").rename(columns={0: "Value"}))

st.markdown("---")
st.caption("※ 그래프 색상: 1등 = 빨간색, 2등~ = 파란색 계열 그라데이션\n※ CSV 파일의 값이 소수(예: 0.07)인 경우 설정에 따라 %로 변환해 보여줍니다.")
