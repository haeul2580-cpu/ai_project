# Streamlit app: 충청북도 분기별 날씨 현황 인터랙티브 대시보드
# 파일명: app.py (이 파일을 Streamlit Cloud에 올리세요)
# 별도: requirements.txt 내용은 파일 끝에 포함

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# --- 설정 ---
st.set_page_config(page_title="충청북도 분기별 날씨", layout="wide")

# 데이터 경로 (업로드 또는 저장된 파일 경로 사용)
DEFAULT_CSV = '충청북도_분기별날씨_프로세스_비율.csv'  # 만약 업로드한 파일이 있다면 이 파일명을 사용

@st.cache_data
def load_data(path=None):
    if path and os.path.exists(path):
        df = pd.read_csv(path, encoding='utf-8-sig')
    else:
        # 만약 프로세스된 파일이 없다면 사용자가 업로드하도록 안내
        st.warning('프로세스된 CSV 파일을 찾을 수 없습니다. 로컬에서 원본 CSV를 업로드해 주세요.')
        uploaded = st.file_uploader('원본 CSV 업로드 (예: 충청북도_분기별날씨현황_20250630.csv)', type=['csv'])
        if uploaded is None:
            return None
        # 자동 인코딩 시도
        encs = ['utf-8','cp949','euc-kr','latin1']
        for e in encs:
            try:
                df = pd.read_csv(uploaded, encoding=e)
                break
            except Exception:
                df = pd.read_csv(uploaded, encoding='utf-8', errors='replace')
                break
    df.columns = df.columns.str.strip()
    return df

# 색 만들기: 1등은 빨강, 그 외는 파란 그라데이션
def make_colors(n):
    colors = []
    for i in range(n):
        if i == 0:
            colors.append('rgba(255,0,0,1)')
        else:
            alpha = max(0.12, 1 - (i * 0.12))
            colors.append(f'rgba(0,0,255,{alpha:.2f})')
    return colors

# 플롯 생성
def make_plot_for_region(df, region_col, category_cols, region):
    pivot = df[[region_col]+category_cols].groupby(region_col).sum()
    prop = pivot.div(pivot.sum(axis=1), axis=0).fillna(0)
    vals = prop.loc[region].sort_values(ascending=False)
    cats = vals.index.tolist()
    numbers = vals.values.tolist()

    colors = make_colors(len(numbers))

    fig = go.Figure()
    fig.add_trace(go.Bar(x=cats, y=numbers, marker_color=colors, text=[f"{v:.1%}" for v in numbers], textposition='auto'))
    fig.update_layout(title=f"지역: {region} — 분기별 비율", xaxis_title='카테고리', yaxis_title='비율', yaxis_tickformat=',.0%')
    return fig


# --- App UI ---
st.title('충청북도 분기별 날씨 현황 대시보드')
st.caption('동네를 선택하면 분기별(혹은 컬럼별) 비율을 보여줍니다. 1등은 빨강, 나머지는 파란 그라데이션으로 표현됩니다.')

df = load_data(DEFAULT_CSV)
if df is None:
    st.stop()

# 자동으로 지역(동네) 컬럼과 카테고리(숫자) 컬럼 감지
possible_region_cols = [c for c in df.columns if any(k in c for k in ['동네','동','지역','시군구','시군','읍','면','구','시','구분'])]
region_col = possible_region_cols[0] if possible_region_cols else None
numeric_cols = df.select_dtypes(include='number').columns.tolist()

st.sidebar.header('설정')
if region_col:
    st.sidebar.write(f'자동 감지된 지역 컬럼: **{region_col}**')
else:
    region_col = st.sidebar.selectbox('지역(동네) 컬럼을 선택하세요', options=df.columns.tolist())

# 사용자가 카테고리 컬럼 선택 가능
if numeric_cols:
    category_cols = st.sidebar.multiselect('비율로 표시할 컬럼들(숫자형)', options=numeric_cols, default=numeric_cols)
else:
    st.error('데이터에 숫자형 컬럼이 없습니다. CSV 형식을 확인하세요.')
    st.stop()

regions = df[region_col].unique().tolist()
sel_region = st.selectbox('동네 선택', options=regions)

# Show raw data sample toggle
if st.checkbox('원본 데이터 보기 (상위 200행)', value=False):
    st.dataframe(df.head(200))

# Plot
fig = make_plot_for_region(df, region_col, category_cols, sel_region)
st.plotly_chart(fig, use_container_width=True)

# 다운로드: 처리된 비율 CSV 생성
if st.button('처리된 비율 CSV 다운로드 생성'):
    pivot = df[[region_col]+category_cols].groupby(region_col).sum()
    prop = pivot.div(pivot.sum(axis=1), axis=0).fillna(0).reset_index()
    out_name = '충청북도_분기별날씨_프로세스_비율_streamlit.csv'
    prop.to_csv(out_name, index=False, encoding='utf-8-sig')
    with open(out_name, 'rb') as f:
        st.download_button('다운로드', f, file_name=out_name)


# ---------------------------
# requirements.txt (Streamlit Cloud에 올릴 때 사용하세요)
# ---------------------------
# 아래 내용을 requirements.txt 파일로 저장하세요
# streamlit
# pandas
# plotly

# End of file
