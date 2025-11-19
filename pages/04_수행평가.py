# 읽기·요약·시각화·Streamlit 앱 파일 생성 (모두 한 번에 실행합니다)
import pandas as pd
import plotly.graph_objects as go
from caas_jupyter_tools import display_dataframe_to_user
import os
from pathlib import Path

# 파일 경로 (사용자 업로드 파일)
file_path = "/mnt/data/충청북도_분기별날씨현황_20250630 (1).csv"

# 1) 파일 로드 (여러 인코딩 시도)
encodings = ['cp949','utf-8','euc-kr','latin1']
df = None
used_enc = None
for e in encodings:
    try:
        df = pd.read_csv(file_path, encoding=e)
        used_enc = e
        break
    except Exception as ex:
        last_ex = ex
if df is None:
    raise last_ex

# 기본 전처리: 컬럼 스트립, 공백 컬럼명 정리
df.columns = df.columns.str.strip()

# 1) 판다스로 꼼꼼하게 살펴보기 (요약)
summary = {
    "파일경로": file_path,
    "사용된_인코딩": used_enc,
    "행수": df.shape[0],
    "열수": df.shape[1],
    "컬럼목록": list(df.columns),
    "데이터타입": df.dtypes.astype(str).to_dict(),
    "결측합계(컬럼별)": df.isna().sum().to_dict(),
    "숫자형_컬럼": df.select_dtypes(include='number').columns.tolist(),
    "비숫자형_컬럼": df.select_dtypes(exclude='number').columns.tolist(),
    "기초통계(숫자형)": df.select_dtypes(include='number').describe().T.reset_index().rename(columns={'index':'컬럼'})
}

# 가능한 지역 컬럼 감지 (예: '구분' 혹은 '동네' 등)
possible_region_cols = [c for c in df.columns if any(k in c for k in ['동네','동','지역','시군구','시군','읍','면','구','시','구분','지역명'])]
region_col = possible_region_cols[0] if possible_region_cols else None

# 가능한 분기/카테고리 컬럼 감지 (분기명 또는 숫자형 컬럼 사용)
quarter_like = [c for c in df.columns if any(q in c.lower() for q in ['q1','q2','q3','q4','1분기','2분기','3분기','4분기','분기'])]
if quarter_like:
    category_cols = quarter_like
else:
    # 숫자형 컬럼들을 카테고리 후보로 사용 (예: '평균기온(섭씨_올해)' 등)
    category_cols = df.select_dtypes(include='number').columns.tolist()

# 구체적 요약 DataFrame 생성 (사람이 보기 쉬운 표)
meta_df = pd.DataFrame([
    ["파일경로", summary["파일경로"]],
    ["사용된 인코딩", summary["사용된_인코딩"]],
    ["행수", summary["행수"]],
    ["열수", summary["열수"]],
    ["자동 감지된 지역 컬럼", region_col],
    ["자동 감지된 카테고리(분기) 컬럼(예시)", ", ".join(category_cols[:10]) if category_cols else "없음"],
    ["숫자형 컬럼 수", len(summary["숫자형_컬럼"])],
    ["비숫자형 컬럼 수", len(summary["비숫자형_컬럼"])],
], columns=["항목", "값"])

# 화면에 원본 데이터와 요약 표시
display_dataframe_to_user("원본 데이터 (상위 200행)", df.head(200))
display_dataframe_to_user("메타 요약", meta_df)
display_dataframe_to_user("숫자형 컬럼 기초 통계", summary["기초통계(숫자형)"].head(200))

# 3) Plotly로 깔끔한 인터랙티브 그래프 생성 (동네 선택 → 분기별 비율)
# 요구사항: 동네를 선택하면 그 동네의 각 카테고리(분기 등) 합을 정규화(비율)하여 표시.
# 색 규칙: 1등 빨강, 2등부터 파랑 그라데이션(투명도 낮아짐)

# 기본적으로 region_col과 category_cols가 있어야 함
if region_col is None or not category_cols:
    raise ValueError("데이터에서 자동으로 지역 컬럼 또는 카테고리(숫자형) 컬럼을 찾지 못했습니다. CSV의 컬럼명을 알려주세요.")

# 그룹화 및 비율 계산
grouped = df[[region_col] + category_cols].groupby(region_col).sum()
proportions = grouped.div(grouped.sum(axis=1), axis=0).fillna(0)  # index=region, cols=categories, values=비율

# 첫 지역 초기값 설정
regions = proportions.index.tolist()
init_region = regions[0]
init_vals = proportions.loc[init_region].sort_values(ascending=False)
cats_order = init_vals.index.tolist()
vals_order = init_vals.values.tolist()

# 색상 생성 함수: 1등 빨강, 나머지 파랑(alpha 감소)
def make_colors_for_values(n):
    colors = []
    for i in range(n):
        if i == 0:
            colors.append('rgba(255,0,0,1)')  # 진한 빨강
        else:
            alpha = max(0.12, 1 - (i * 0.12))
            colors.append(f'rgba(0,0,255,{alpha:.2f})')
    return colors

init_colors = make_colors_for_values(len(vals_order))

fig = go.Figure()
fig.add_trace(go.Bar(x=cats_order, y=vals_order, marker_color=init_colors, text=[f"{v:.1%}" for v in vals_order], textposition='auto'))

# Dropdown 버튼(지역 선택) 추가
buttons = []
for reg in regions:
    sorted_vals = proportions.loc[reg].sort_values(ascending=False)
    vals = sorted_vals.values.tolist()
    cats = sorted_vals.index.tolist()
    cols = make_colors_for_values(len(vals))
    buttons.append(dict(method='update',
                        label=str(reg),
                        args=[{'x': [cats], 'y': [vals], 'marker.color': [cols], 'text': [[f"{v:.1%}" for v in vals]]},
                              {'title': f"{reg} — 분기별 비율 (정규화)"}]))

fig.update_layout(
    title=f"{init_region} — 분기별 비율 (정규화)",
    updatemenus=[dict(active=0, buttons=buttons, x=0.0, xanchor='left', y=1.15, yanchor='top')],
    xaxis_title="카테고리(분기 등)",
    yaxis_title="비율",
    yaxis_tickformat=',.0%',
    margin=dict(t=120)
)

# Plotly 그래프 출력
fig.show()

# 2) Streamlit Cloud에서 작동되는 코드 생성 (app.py) — 파일로 저장
app_code = f'''import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="충청북도 분기별 날씨", layout="wide")

DATA_FILE = "충청북도_분기별날씨현황_20250630 (1).csv"

@st.cache_data
def load_data(path=DATA_FILE):
    # 여러 인코딩 시도
    encs = ['cp949','utf-8','euc-kr','latin1']
    last = None
    for e in encs:
        try:
            df = pd.read_csv(path, encoding=e)
            return df
        except Exception as ex:
            last = ex
    # 마지막으로 강제 읽기 (errors='replace')
    return pd.read_csv(path, encoding='utf-8', errors='replace')

df = load_data()

df.columns = df.columns.str.strip()

# 자동 감지: 지역 컬럼 (예: '구분' 등) 및 숫자형 카테고리 컬럼
possible_region_cols = [c for c in df.columns if any(k in c for k in ['동네','동','지역','시군구','시군','읍','면','구','시','구분','지역명'])]
region_col = possible_region_cols[0] if possible_region_cols else st.sidebar.selectbox("지역 컬럼을 선택하세요", df.columns.tolist())

numeric_cols = df.select_dtypes(include='number').columns.tolist()
if not numeric_cols:
    st.error("숫자형 컬럼(분기/카테고리)이 없습니다. CSV를 확인하세요.")
    st.stop()

st.title("충청북도 분기별 날씨 현황 대시보드")
st.sidebar.header("설정")
st.sidebar.write(f"자동 감지된 지역 컬럼: **{region_col}**")

category_cols = st.sidebar.multiselect("비율로 표시할 컬럼들(숫자형)", options=numeric_cols, default=numeric_cols)

regions = df[region_col].unique().tolist()
sel_region = st.selectbox("동네 선택", regions)

# 비율 계산
grouped = df[[region_col] + category_cols].groupby(region_col).sum()
prop = grouped.div(grouped.sum(axis=1), axis=0).fillna(0)

vals_sorted = prop.loc[sel_region].sort_values(ascending=False)
cats = vals_sorted.index.tolist()
vals = vals_sorted.values.tolist()

# 색상 설정: 1등 빨강, 나머지 파랑 그라데이션
def make_colors(n):
    colors = []
    for i in range(n):
        if i == 0:
            colors.append('rgba(255,0,0,1)')
        else:
            alpha = max(0.12, 1 - (i * 0.12))
            colors.append(f'rgba(0,0,255,{alpha:.2f})')
    return colors

colors = make_colors(len(vals))

fig = go.Figure()
fig.add_trace(go.Bar(x=cats, y=vals, marker_color=colors, text=[f\"{v:.1%}\" for v in vals], textposition='auto'))
fig.update_layout(title=f\"{sel_region} — 분기별 비율\", xaxis_title='카테고리', yaxis_title='비율', yaxis_tickformat=',.0%')

st.plotly_chart(fig, use_container_width=True)

if st.checkbox('원본 데이터 보기'):
    st.dataframe(df.head(200))

# 다운로드: 처리된 비율 CSV
if st.button('처리된 비율 CSV 생성 및 다운로드'):
    out = prop.reset_index()
    out_name = '충청북도_분기별날씨_프로세스_비율.csv'
    out.to_csv(out_name, index=False, encoding='utf-8-sig')
    with open(out_name, 'rb') as f:
        st.download_button('다운로드', f, file_name=out_name)
'''

app_path = "/mnt/data/app.py"
with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_code)

# requirements.txt 생성
reqs = "streamlit\npandas\nplotly\nnumpy\n"
req_path = "/mnt/data/requirements.txt"
with open(req_path, "w", encoding="utf-8") as f:
    f.write(reqs)

# 처리된 비율 CSV 저장
processed_path = "/mnt/data/충청북도_분기별날씨_프로세스_비율.csv"
proportions.reset_index().to_csv(processed_path, index=False, encoding='utf-8-sig')

# 6) 리콰이어(=requirements.txt) 이미 생성됨

# 출력 요약
print("== 작업 완료 요약 ==")
print("원본 파일 경로:", file_path)
print("사용 인코딩:", used_enc)
print("행,열:", df.shape)
print("자동 감지된 지역 컬럼:", region_col)
print("카테고리(숫자) 컬럼 예시:", category_cols[:10] if 'category_cols' in locals() else '자동검출없음')
print("생성된 파일:")
print(" - Streamlit 앱 코드:", app_path)
print(" - requirements.txt:", req_path)
print(" - 처리된 비율 CSV:", processed_path)

# 사용자에게 다운로드 가능한 경로 알림 (python_user_visible는 실행파일을 만들어줌)
download_links = {
    "app.py": app_path,
    "requirements.txt": req_path,
    "processed_csv": processed_path,
    "original_csv": file_path
}

download_links

