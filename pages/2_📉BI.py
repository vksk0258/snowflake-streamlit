import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

conn = st.connection("snowflake")

QUALIFIED_TABLE_NAME = "FROSTY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ANNUAL_TIME_SERIES"
table = QUALIFIED_TABLE_NAME.split(".")

df = conn.query(f"SELECT * FROM {QUALIFIED_TABLE_NAME}")

df_total = df[df['VARIABLE_NAME'].str.contains('Total Assets')]

# ENTITY_NAME을 기준으로 선택할 수 있는 selectbox 생성
city_name = st.selectbox('CITY 선택', df_total['CITY'].unique())
filtered_df_city = df_total[df_total['CITY'] == city_name]


entity_name = st.selectbox('Entity 선택', filtered_df_city['ENTITY_NAME'].unique())
filtered_df = filtered_df_city[filtered_df_city['ENTITY_NAME'] == entity_name].sort_values(by=['YEAR'], axis=0)


# 선 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(filtered_df['YEAR'], filtered_df['VALUE'], marker='o')
plt.title(f'YEAR 별 VALUE 변화 추이 ({entity_name})')
plt.xlabel('YEAR')
plt.ylabel('VALUE')
plt.grid(True)

# Streamlit에 그래프 출력
st.pyplot(plt)


