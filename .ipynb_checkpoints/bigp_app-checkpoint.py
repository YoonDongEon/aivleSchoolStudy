# 웹캠 실행을 위해 따로 설치해야 하는 모듈
# 1. pip install streamlit-webrtc
# 2. pip install torchvision

# 모듈 선언
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import joblib
from keras.models import load_model
from haversine import haversine
from urllib.parse import quote
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium
import folium
from folium.features import DivIcon
import branca
from geopy.geocoders import Nominatim
import ssl
from urllib.request import urlopen
import altair as alt
import plotly.express as px
import time
import folium
from io import BytesIO
from PIL import Image
import cv2
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer, WebRtcMode, RTCConfiguration
import torch
import av
from folium.plugins import MarkerCluster
from folium.plugins import MiniMap
import json
import math

# 기본 세팅
st.set_page_config(layout="wide")
pd.set_option('display.max.colwidth', 50)
st.markdown("""
<style>
.st-emotion-cache-16idsys p {
    font-size: 18px;
}
.st-emotion-cache-183lzff {
    font-size: 18px;
}
.st-emotion-cache-5rimss p {
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# 로딩
with st.spinner('Wait for it...'):
    time.sleep(3)

# 아이콘
ic1, ic_empty, ic2 = st.columns([0.2, 0.4, 0.05])
with ic1:
    image_file1 = '솔루션로고(임시).jpg'
    image_local1 = Image.open(image_file1)
    st.image(image_local1, width=150)
with ic_empty:
    st.caption("")
    st.markdown("# 시각장애인을 위한 스마트 자동 판매기 솔루션")
with ic2:
    image_file2 = '01_KT Wordmark (Standard)_01.jpg'
    image_local2 = Image.open(image_file2)
    st.image(image_local2, width=150)

# 관련 데이터셋
df1 = pd.read_csv('식품자동판매기_장애인이용현황.csv', encoding='cp949')
df2 = pd.read_csv('국내 시각장애인 수 현황.csv', encoding='cp949', index_col=0)
state_geo = './ctprvn.json'

# 시도기준 경계 JSON 파일을 들고 온다.
with open(state_geo, encoding='utf-8') as file:
    sido_map = json.load(file)

# 대시보드를 3개 탭으로 나누기
tab1, tab2, tab3 = st.tabs(["장애인 자동판매기 맵", "장애인 복지관 관련 현황", "시각장애인 모니터링"])

### ------------------------------------------------ ▼ 장애인 복지관 맵 코딩 시작 ▼ ------------------------------------------------
with tab1:
    # 초기 지도 표시 위치
    my_map = folium.Map( location=[df1['좌표정보(x)'].mean()+0.3, df1['좌표정보(y)'].mean()+0.8], zoom_start=7)
    marker_cluster = MarkerCluster().add_to(my_map)  # 클러스터 추가하기
    minimap = MiniMap(toggle_display=True, position='topleft', width=150, height=150)
    minimap.add_to(my_map)
    # 위도경도 매핑
    locs = {
        '경기도': (37.95, 126.95),
        '서울특별시': (37.58, 126.7),
        '부산광역시':(35.198362, 129.053922),
        '경상북도':  (36.63, 128.46),
        '경상남도': (35.5, 128),
        '인천광역시':  (37.5, 125.8),
        '대구광역시': (35.96, 128.32),
        '충청남도': (36.69, 126),
        '전라남도':  (34.819400, 126.893113),
        '전라북도':  (35.86, 126.85),
        '대전광역시':   (36.321655, 127.378953),
        '강원도': (37.88, 128),
        '광주광역시': (35.28, 126.49),
        '울산광역시': (35.8, 129.5),
        '충청북도': (37.19, 127.50),
        '세종특별자치시':    (36.7, 127.07),
        '제주특별자치도':   (33.62, 126.11),
    }
    
    big_layout1, big_layout2 = st.columns([1,1])
    # 장애인 복지관 현황 지도
    with big_layout1:
        st.markdown("## 식품자동판매기 장애인이용현황 맵")
        now = datetime.datetime.now()  # 현재 시간을 가져옵니다.
        now_str = now.strftime("%Y-%m-%d %H:%M")
        st.text(now_str)

        # 시설명 리스트
        relief_cente_list = df1['사업장명']
        # 복지관 검색 박스
        relief_center_search = st.text_input('사업장명을 검색하세요.', value='', max_chars=20, help='20자 이내로만 입력가능합니다.')
        people_slider_range = st.slider('이용현황을 확인할 연도를 선택해주세요.', 2013, 2022, 2022, 1)
        
        # 검색어가 입력되었다면
        if relief_center_search !='':
            # 검색어를 포함하는 항목만 필터링합니다.
            results = [item for item in relief_cente_list if relief_center_search in item]
            
            # 결과를 출력합니다.
            st.write(f"Results for '{relief_center_search}':")
            search_df1 = df1[df1['사업장명'].isin(results)]
            for idx, row in search_df1.iterrows():
                html= """<!DOCTYPE html>
                <html>
                        <table style="height: 160px; width: 350px;"> <tbody> <tr>
                        <td style="background-color: #2A799C;">
                        <div style="width: 140px;color: #ffffff;text-align:center;">사업장명</div></td>
                        <td style="width: 230px;background-color: #C5DCE7;">{}</td>""".format(row['사업장명'])+"""</tr>
                        <tr><td style="background-color: #2A799C;">
                        <div style="width: 140px;color: #ffffff;text-align:center;">사업장 주소</div></td>
                        <td style="width: 230px;background-color: #C5DCE7;">{}</td>""".format(row['소재지전체주소'])+"""</tr>
                        <tr><td style="background-color: #2A799C;">
                        <div style="width: 140px;color: #ffffff;text-align:center;">전화번호</div></td>
                        <td style="width: 230px;background-color: #C5DCE7;">{}</td>""".format(row['소재지전화'])+"""</tr>
                        <tr><td style="background-color: #2A799C;">
                        <div style="width: 140px;color: #ffffff;text-align:center;">자판기 이용률</div></td>
                        <td style="width: 230px;background-color: #C5DCE7;">{}</td>""".format(str(row['이용률'])+'%')+"""</tr>
                    </tbody> </table> </html> """
                iframe= branca.element.IFrame(html=html, width=360, height=160)
                popup_text= folium.Popup(iframe,parse_html=True)
                if row['이용률'] >= 100:
                    icon= folium.Icon(icon='home', color="blue")
                elif row['이용률'] < 100:
                    icon= folium.Icon(icon='home', color="red")
                folium.Marker(location=[row['좌표정보(x)'], row['좌표정보(y)']], 
                            popup=popup_text, tooltip=row['사업장명'], icon=icon).add_to(marker_cluster)
            ch = folium.Choropleth(
                # geo json 파일로 sido_map 을 사용
                geo_data=sido_map,
                # choropleth 옵션을 쓸 것임
                name='choropleth',
                # data로는 population.csv 파일을 사용 (df로 불러옴)
                data=df2,
                # csv 파일에서 사용할 컬럼 값
                columns=['시도별', str(people_slider_range)], 
                # 시도명 - CTP_KOR_NM 매핑
                key_on='feature.properties.CTP_KOR_NM',
                # geo json 색깔 설정
                fill_color='Spectral',
                # 지도 투명하게  
                fill_opacity=0.7,
                # 경계선 투명하게
                line_opacity=1,  
                # 경계선 굵기
                line_weight=1.5,
                # 경계선 색
                line_color='#000',
                # 범례 이름
                legend_name='시도별 복지관 내 시각장애인 수(명)',  
                #  highlight=True, # 하이라이트 설정
            ).add_to(my_map)
            for key, value in locs.items():
                folium.map.Marker(
                    # 위경도 위치
                    [value[0], value[1]],  

                    # DivIcon 을 사용
                    # html 태그를 이용해서 text를 올릴 수 있음
                    icon=DivIcon(
                        # icon px 사이즈
                        icon_size=(0, 0),
                        # icon 좌 상단 위치 설정
                        icon_anchor=(0, 0),

                        # html 형식으로 text 추가
                        # div 태그 안에 style 형식 추가
                        html='<div\
                                style="\
                                    font-size: 1.2rem;\
                                    color: black;\
                                    background-color:rgba(255, 255, 255, 0.2);\
                                    width:85px;\
                                    text-align:center;\
                                    margin:0px;\
                                "><b>'
                        + key + ': ' + str(''.join(str(df2.loc[(df2['시도별']==key), str(people_slider_range)].values.sum())))
                        + '</b></div>',
                    )).add_to(my_map)
            st_data= st_folium(my_map, width=1050, height=1000)
        # 검색어가 빈칸으로 입력되었다면
        elif relief_center_search =='':
            for idx, row in df1.iterrows():
                html= """<!DOCTYPE html>
                <html>
                        <table style="height: 160px; width: 350px;"> <tbody> <tr>
                        <td style="background-color: #2A799C;">
                        <div style="width: 140px;color: #ffffff;text-align:center;">사업장명</div></td>
                        <td style="width: 230px;background-color: #C5DCE7;">{}</td>""".format(row['사업장명'])+"""</tr>
                        <tr><td style="background-color: #2A799C;">
                        <div style="width: 140px;color: #ffffff;text-align:center;">사업장 주소</div></td>
                        <td style="width: 230px;background-color: #C5DCE7;">{}</td>""".format(row['소재지전체주소'])+"""</tr>
                        <tr><td style="background-color: #2A799C;">
                        <div style="width: 140px;color: #ffffff;text-align:center;">전화번호</div></td>
                        <td style="width: 230px;background-color: #C5DCE7;">{}</td>""".format(row['소재지전화'])+"""</tr>
                        <tr><td style="background-color: #2A799C;">
                        <div style="width: 140px;color: #ffffff;text-align:center;">자판기 이용률</div></td>
                        <td style="width: 230px;background-color: #C5DCE7;">{}</td>""".format(str(row['이용률'])+'%')+"""</tr>
                    </tbody> </table> </html> """
                iframe= branca.element.IFrame(html=html, width=360, height=160)
                popup_text= folium.Popup(iframe,parse_html=True)
                if row['이용률'] >= 100:
                    icon= folium.Icon(icon='home', color="blue")
                elif row['이용률'] < 100:
                    icon= folium.Icon(icon='home', color="red")
                folium.Marker(location=[row['좌표정보(x)'], row['좌표정보(y)']], 
                            popup=popup_text, tooltip=row['사업장명'], icon=icon).add_to(marker_cluster)
            ch = folium.Choropleth(
                # geo json 파일로 sido_map 을 사용
                geo_data=sido_map,
                # choropleth 옵션을 쓸 것임
                name='choropleth',
                # data로는 population.csv 파일을 사용 (df로 불러옴)
                data=df2,
                # csv 파일에서 사용할 컬럼 값
                columns=['시도별', str(people_slider_range)], 
                # 시도명 - CTP_KOR_NM 매핑
                key_on='feature.properties.CTP_KOR_NM',
                # geo json 색깔 설정
                fill_color='Spectral',
                # 지도 투명하게  
                fill_opacity=0.5,
                # 경계선 투명하게
                line_opacity=1,  
                # 경계선 굵기
                line_weight=1.5,
                # 경계선 색
                line_color='#000',
                # 범례 이름
                legend_name='시도별 복지관 내 시각장애인 수(명)',  
                #  highlight=True, # 하이라이트 설정
            ).add_to(my_map)
            
            for key, value in locs.items():
                folium.map.Marker(
                    # 위경도 위치
                    [value[0], value[1]],  

                    # DivIcon 을 사용
                    # html 태그를 이용해서 text를 올릴 수 있음
                    icon=DivIcon(
                        # icon px 사이즈
                        icon_size=(0, 0),
                        # icon 좌 상단 위치 설정
                        icon_anchor=(0, 0),

                        # html 형식으로 text 추가
                        # div 태그 안에 style 형식 추가
                        html='<div\
                                style="\
                                    font-size: 1.2rem;\
                                    color: black;\
                                    background-color:rgba(255, 255, 255, 0.2);\
                                    width:85px;\
                                    text-align:center;\
                                    margin:0px;\
                                "><b>'
                        + key + ': ' + str(''.join(str(df2.loc[(df2['시도별']==key), str(people_slider_range)].values.sum())))
                        + '</b></div>',
                    )).add_to(my_map)
            st_data= st_folium(my_map, width=1050, height=1000)                                                                             
    
    # 유형별 장애인 수 차트
    with big_layout2:
        st.markdown("## 국내 시각장애인 수")
        st.text("유형 선택")
        
        col160, col161 = st.columns([0.2, 0.8])
        # 시도별 옵션
        with col160:
            st.info("시도별")
        with col161:
            # 시도별 체크박스 생성
            city_check = st.multiselect('', df2['시도별'].unique(), key='2', label_visibility="collapsed")

        col170, col171 = st.columns([0.2, 0.8])
        # 성별 옵션
        with col170:
            st.info("성별")
        with col171:
             # 성별 체크박스 생성
            gender_check = st.multiselect('', df2['성별'].unique(), key='3', label_visibility="collapsed")

        col180, col181 = st.columns([0.2, 0.8])
        # 성별 옵션
        with col180:
            st.info("검색년도")
        with col181:
            # 검색년도 옵션
            slider_range = st.slider('', 2013, 2022, 2022, 1, label_visibility="collapsed")

        # 선택한 값에 따라 데이터 필터링
        filtered_df = df2[df2['시도별'].isin(city_check) & df2['성별'].isin(gender_check)]
        
        medium_empty1, medium_layout1, medium_layout2, medium_empty2 = st.columns([1, 4, 4, 1])

        # 시도별 장애인 수 파이 차트
        with medium_layout1:
            fig = px.pie(filtered_df, names='시도별', values=str(slider_range), 
                title='시도별 장애인 수'+'('+str(slider_range)+'년도 기준'+')',
                         color_discrete_sequence=px.colors.qualitative.Pastel1, width=450, height=450, hole=.2)

            fig.update_traces(textposition='inside', textinfo='percent+label+value')
            fig.update_layout(font=dict(size=15))
            fig.update(layout_showlegend=False) # 범례표시 제거

            st.plotly_chart(fig)
        # 성별 장애인 수 파이 차트
        with medium_layout2:
            fig = px.pie(filtered_df, names='성별', values=str(slider_range), 
                title='성별 장애인 수'+'('+str(slider_range)+'년도 기준'+')',
                         color_discrete_sequence=px.colors.qualitative.Pastel2, width=450, height=450, hole=.2)

            fig.update_traces(textposition='inside', textinfo='percent+label+value')
            fig.update_layout(font=dict(size=15))
            fig.update(layout_showlegend=False) # 범례표시 제거

            st.plotly_chart(fig)
        with st.expander(label='검색 결과 상세보기'):
            expander_layout1, empty, expander_layout2 = st.columns([0.6, 0.1, 0.3])
            with expander_layout1:
                st.table(filtered_df[['시도별', '성별', str(slider_range)]])
            # 결과물에 대한 다운로드 옵션(csv, 엑셀)
            with expander_layout2:
                # csv 형태로 다운로드
                csv_data = filtered_df[['시도별', '성별', str(slider_range)]].to_csv().encode('cp949')
                st.subheader("CSV 파일로 다운로드")
                st.download_button("CSV 파일 다운로드", csv_data, file_name='국내 시각장애인 수('+str(slider_range)+').csv')
                st.subheader(" ")
                # 엑셀(xlsx) 형태로 다운로드
                excel_data = BytesIO()
                filtered_df[['시도별', '성별', str(slider_range)]].to_excel(excel_data)
                st.subheader("엑셀 파일로 다운로드")
                st.download_button("엑셀 파일 다운로드", excel_data, file_name='국내 시각장애인 수('+str(slider_range)+').xlsx')
                
        st.markdown("## 예상 수익 현황")
        st.text("단위: 자동 판매기 이용자 100명")
            
        col190, col191, col192, col193 = st.columns([0.25, 0.25, 0.25, 0.25])
        with col190:
            st.metric(label="1일 판매량", value=str(format(math.trunc((14.91+9.94+9.94+4.97+4.97)*100), ',')) +' 개', delta="65 %")
        with col191:
            st.metric(label="1일 매출액", value=str(format((4473+5964+7952+5964+9939)*100, ',')) +' 원', delta="65 %")
        with col192:
            st.metric(label="1일 순이익", value=str(format((3280+3479+4473+2982+4970)*100, ',')) +' 원', delta="65 %")
        with col193:
            st.metric(label="월 예측 판매 수익", value=str(format(420983, ','))+' 원', delta="108 %")
        
### ------------------------------------------------ ▲ 장애인 복지관 맵 코딩 끝 ▲ ------------------------------------------------

### -------------------------------------------- ▼ 장애인 복지관 관련 현황 코딩 시작 ▼ --------------------------------------------
with tab2:
    col250, empty250, col251 = st.columns([3, 6, 1])
    with col250:
        st.markdown("## 장애인 복지관 관련 현황")
    with col251:
        st.subheader("Power BI")
    
    # 관련 현황을 나타내는 PowerBI와 연동
    iframe_code = '''
    <iframe title="빅프로젝트_분석" width="2000" height="1000" src="https://app.powerbi.com/reportEmbed?reportId=127df1e4-c588-4f6c-a1b4-c31e3d651eb0&autoAuth=true&ctid=a633bbdc-0cc6-4cb1-8bba-7fa0ea11b482" frameborder="1" allowFullScreen="True"></iframe>
    '''
    
    # 스트림릿 앱에 파워BI 리포트를 임베드합니다.
    components.html(iframe_code, height=1000)
    
    col252, empty251 = st.columns([5, 5])
    with col252:
        with st.expander(label='보고서 다운로드'):
            col260, col261 = st.columns([3, 3])
            with col260:
                st.subheader("PDF 파일로 다운로드")
                st.download_button("PDF 파일 다운로드", "빅프로젝트_분석.pdf", file_name='장애인 복지관 관련 현황.pdf')
            with col261:
                st.subheader("파워포인트 파일로 다운로드")
                st.download_button("파워포인트 파일 다운로드", '빅프로젝트_분석.pptx', file_name='장애인 복지관 관련 현황.pptx')
    
### --------------------------------------------- ▲ 장애인 복지관 관련 현황 코딩 끝 ▲ ---------------------------------------------

### ---------------------------------------------- ▼ 시각장애인 모니터링 코딩 시작 ▼ ----------------------------------------------
with tab3:
    st.markdown("## 시각장애인 모니터링")
    monitoring_empty1, monitoring1, monitoring_empty1 = st.columns([1, 4, 1])
    device = 'cpu'
    if not hasattr(st, 'classifier'):
        st.model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', _verbose=False)

    RTC_CONFIGURATION = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    class VideoProcessor:
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")

            # vision processing
            
            # model processing
            im_pil = Image.fromarray(img)
            results = st.model(im_pil)
            bbox_img = np.array(results.render()[0])

            return av.VideoFrame.from_ndarray(bbox_img, format="bgr24")
    
    with monitoring1:
        webrtc_ctx = webrtc_streamer(
                key="monitoring",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration=RTC_CONFIGURATION,
                video_processor_factory=VideoProcessor,
                media_stream_constraints={
                    "video": True,
                    "audio": False
                },
                async_processing=True,
            )

### ----------------------------------------------- ▲ 시각장애인 모니터링 코딩 끝 ▲ -----------------------------------------------