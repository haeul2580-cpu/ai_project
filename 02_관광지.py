# Streamlit app: Seoul Top10 (folium)
# Filename: app.py (copy this into your Streamlit Cloud repo as app.py)
# Also included below: requirements.txt content (copy into a file named requirements.txt)
# Quick deploy steps:
# 1. Create a new GitHub repo (or use an existing one).
# 2. Add app.py (this file) and requirements.txt to the repo root.
# 3. Connect the repo in https://share.streamlit.io and deploy.

import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Seoul Top10 — Folium", layout="wide")
st.title("Seoul — Top 10 Tourist Spots (popular with foreigners)")
st.markdown("간단한 Folium 지도 + 마커 클러스터 예제입니다. 아래 설정을 바꿔 보세요.")

# Top 10 list: (name, lat, lon, short description)
TOP10 = [
    ("Gyeongbokgung Palace", 37.579884, 126.9768, "Historic Joseon royal palace — must-see."),
    ("N Seoul Tower (Namsan)", 37.551170, 126.988228, "Iconic observatory with panoramic city views."),
    ("Myeong-dong", 37.563183, 126.98535, "Shopping & street food hotspot."),
    ("Bukchon Hanok Village", 37.579956, 126.982089, "Traditional hanok neighborhood for photos."),
    ("Insadong", 37.574353, 126.984355, "Art, tea houses and crafts — cultural street."),
    ("Hongdae (Hongik University area)", 37.55528, 126.92333, "Youth culture, cafés, live music, street art."),
    ("Dongdaemun Design Plaza (DDP)", 37.5663, 127.0090, "Futuristic architecture, night shopping."),
    ("Changdeokgung Palace & Huwon", 37.5826, 126.9910, "UNESCO palace with secret garden (Huwon)."),
    ("Cheonggyecheon Stream", 37.5702, 126.9768, "Urban stream restoration, pleasant walk."),
    ("Lotte World Tower (Seoul Sky)", 37.5130, 127.1025, "Tall skyscraper with observation deck.")
]

# Sidebar controls
st.sidebar.header("Map settings")
start_zoom = st.sidebar.slider("Initial zoom", 10, 14, 12)
show_cluster = st.sidebar.checkbox("Use marker cluster", True)
show_list = st.sidebar.checkbox("Show list of spots below map", True)
center_lat = st.sidebar.number_input("Center latitude", value=37.5665, format="%.6f")
center_lon = st.sidebar.number_input("Center longitude", value=126.9780, format="%.6f")

# Create folium map
m = folium.Map(location=[center_lat, center_lon], zoom_start=start_zoom)

# Tile layers
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)
folium.TileLayer('Stamen Toner', name='Stamen Toner').add_to(m)
folium.TileLayer('CartoDB positron', name='CartoDB Positron').add_to(m)

if show_cluster:
    cluster = MarkerCluster().add_to(m)
    for name, lat, lon, desc in TOP10:
        popup_html = f"<b>{name}</b><br>{desc}<br><i>좌표: {lat}, {lon}</i>"
        folium.Marker(location=[lat, lon], popup=popup_html, tooltip=name).add_to(cluster)
else:
    for name, lat, lon, desc in TOP10:
        popup_html = f"<b>{name}</b><br>{desc}<br><i>좌표: {lat}, {lon}</i>"
        folium.Marker(location=[lat, lon], popup=popup_html, tooltip=name).add_to(m)

# Add layer control
folium.LayerControl(collapsed=False).add_to(m)

# Render map in Streamlit
with st.spinner("Loading map..."):
    st_data = st_folium(m, width=1200, height=700)

# Optional list view
if show_list:
    st.markdown("---")
    st.subheader("Top 10 — Quick list")
    cols = st.columns(2)
    for i, (name, lat, lon, desc) in enumerate(TOP10, start=1):
        col = cols[(i-1) % 2]
        col.markdown(f"**{i}. {name}**  
- {desc}  
- 좌표: `{lat}, {lon}`")

st.markdown("---")
st.caption("데이터 출처: 공개 관광/여행 가이드(Tripadvisor, VisitSeoul 등) 및 위키피디아. 좌표는 일반적으로 공개된 위치 정보를 사용했습니다.")

# Footer: copy & download
st.markdown("### Get the code & requirements")
st.code("""
# app.py (this file)
# requirements.txt (copy the content from the repo file)
""", language='python')


# ---- requirements.txt content (copy this into requirements.txt in your repo) ----
# Streamlit Cloud needs this to install dependencies
REQUIREMENTS_TXT = """
streamlit>=1.24
folium>=0.14
streamlit-folium>=0.14.0
branca>=0.6
"""

st.download_button("Download requirements.txt", REQUIREMENTS_TXT, file_name="requirements.txt")

# End of app.py

# ==================================================================
# If you copied this into a file named app.py and created requirements.txt
# as shown above, deploy to Streamlit Cloud by linking your GitHub repo.
# ==================================================================
