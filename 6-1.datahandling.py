import streamlit as st
import pandas as pd

st.text('1. 지하철 데이터 읽고 확인- data_subway_in_seoul.csv')   
# streamlit\data_subway_in_seoul.csv
# encoding='cp949'  읽어오고 확인하기 
df = pd.read_csv('data_subway_in_seoul.csv', encoding='cp949')
st.dataframe(df)

st.text("2. 구분이 '하차'인 행만 새로운 데이터프레임으로 저장 & 확인") 
df_off = df.loc[df['구분']=='하차']
st.dataframe(df_off)

st.text("3. '날짜','연번','역번호','역명','구분','합계' 제외하고 저장 & 확인")
df_line = df_off[df_off.columns.difference(['날짜', '연번', '역번호', '역명', '구분', '합계', '제외하고 저장 & 확인'])]
st.dataframe(df_line)

st.text("4. 아래 방법으로 데이터프레임 변환하여 저장 & 확인")
st.caption("melt 함수 사용 unpivot: identifier-'호선', unpivot column-'시간', value column-'인원수'")
df_line_melted = pd.melt(df_line, id_vars=['호선'], var_name='시간', value_name='인원수')
st.dataframe(df_line_melted)

st.text("5. '호선','시간' 별 '인원수' 합,  as_index=False 저장 & 확인")
df_line_groupby = df_line_melted.groupby(['호선', '시간'], as_index=False)['인원수'].count()
st.dataframe(df_line_groupby)


# 파일실행: File > New > Terminal(anaconda prompt) - streamlit run streamlit\6-1.datahandling.py