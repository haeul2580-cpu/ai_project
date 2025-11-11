import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Seoul Top10 — Folium", layout="wide")
st.title("🇰🇷 Seoul — Top 10 Tourist Spots Loved by Foreigners")
st.markdown("서울의 대표적인 관광 명소 10곳을 지도로 표시하고, 아래에 간단한 소개와 가까운 전철역을 함께 정리했습니다.")

# Top 10 list: (name, lat, lon, description, nearby_station)
TOP10 = [
    ("Gyeongbokgung Palace", 37.579884, 126.9768, "조선의 법궁으로, 아름다운 전통 건축과 경회루가 있는 명소.", "경복궁역 5호선"),
    ("N Seoul Tower (Namsan)", 37.551170, 126.988228, "서울 전경을 한눈에 볼 수 있는 전망대이자 야경 명소.", "명동역 4호선"),
    ("Myeong-dong", 37.563183, 126.98535, "외국인 관광객에게 인기 있는 쇼핑 거리와 길거리 음식 천국.", "명동역 4호선"),
    ("Bukchon Hanok Village", 37.579956, 126.982089, "전통 한옥이 즐비한 골목길로, 서울의 옛 정취를 느낄 수 있는 곳.", "안국역 3호선"),
    ("Insadong", 37.574353, 126.984355, "전통 공예품과 찻집, 갤러리가 모여 있는 문화 거리.", "종로3가역 1·3·5호선"),
    ("Hongdae (Hongik University area)", 37.55528, 126.92333, "젊음의 거리로, 예술·음악·패션이 어우러진 활기찬 지역.", "홍대입구역 2호선"),
    ("Dongdaemun Design Plaza (DDP)", 37.5663, 127.0090, "미래형 디자인 건축물로, 패션과 야시장이 유명한 명소.", "동대문역사문화공원역 2·4·5호선"),
    ("Changdeokgung Palace & Huwon", 37.5826, 126.9910, "비밀의 정원 후원을 품은 유네스코 세계문화유산 궁궐.", "안국역 3호선"),
    ("Cheonggyecheon Stream", 37.5702, 126.9768, "도심 속 하천으로, 산책하기 좋은 서울의 대표 휴식공간.", "광화문역 5호선"),
    ("Lotte World Tower (Seoul Sky)", 37.5130, 127.1025, "555m 초고층 전망대와 쇼핑몰, 호텔이 함께 있는 복합 랜드마크.", "잠실역 2·8호선")
]

# Sidebar
st.sidebar.header("Map Settings")
zoom = st.sidebar.slider("Zoom", 10, 14, 12)
center_lat = st.sidebar.number_input("Center latitude", value=37.5665, format="%.6f")
center_lon = st.sidebar.number_input("Center longitude", value=126.9780, format="%.6f")

# Map creation
m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles='CartoDB positron')

# Add markers (red color)
for name, lat, lon, desc, station in TOP10:
    popup_html = f"<b>{name}</b><br>{desc}<br><i>📍 가까운 전철역: {station}</i>"
    folium.Marker(location=[lat, lon], popup=popup_html, tooltip=name, icon=folium.Icon(color='red')).add_to(m)

# Display map (80% width)
st.markdown("---")
st_folium(m, width=960, height=560)

# Below map — introduction
st.markdown("---")
st.subheader("🗺️ 서울 Top10 관광지 간단 소개")

for i, (name, lat, lon, desc, station) in enumerate(TOP10, start=1):
    st.markdown(f"**{i}. {name}**  
- {desc}  
- 🚇 **가까운 전철역:** {station}\n")

st.markdown("---")
st.caption("자료 출처: VisitSeoul, TripAdvisor, Google Maps 등 공개 관광 정보 기반.")
