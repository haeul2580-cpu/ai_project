# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium

st.title("🇫🇷 한국인이 좋아하는 프랑스 관광지 TOP10 지도")

# 관광지 데이터
data = [
    ("에펠탑", 48.8584, 2.2945),
    ("루브르 박물관", 48.8606, 2.3376),
    ("몽마르트르 언덕", 48.8867, 2.3431),
    ("노트르담 대성당", 48.8529, 2.3500),
    ("베르사유 궁전", 48.8049, 2.1204),
    ("몽생미셸", 48.6361, -1.5115),
    ("샹젤리제 거리", 48.8698, 2.3076),
    ("오르세 미술관", 48.8600, 2.3266),
    ("라데팡스", 48.8924, 2.2369),
    ("니스 해변", 43.6950, 7.2718)
]

m = folium.Map(location=[48.8566, 2.3522], zoom_start=6)

for name, lat, lon in data:
    folium.Marker([lat, lon], tooltip=name, popup=name, icon=folium.Icon(color="red")).add_to(m)

st_folium(m, width=700, height=500)


# ---- requirements.txt ----
# streamlit
# folium
# streamlit-folium
