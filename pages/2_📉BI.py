import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(page_title = "GA Dashboard", 
    page_icon = "🎲", 
    layout = "wide", 
    initial_sidebar_state = "auto" 
    )

conn = st.connection("snowflake")

QUALIFIED_TABLE_NAME = "FROSTY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ANNUAL_TIME_SERIES"
table = QUALIFIED_TABLE_NAME.split(".")

df = conn.query(f"SELECT * FROM {QUALIFIED_TABLE_NAME}")

df_total = df[df['VARIABLE_NAME'].str.contains('Total Assets')]

col11, col12, col13 = st.columns([0.34, 0.33, 0.33])

# ENTITY_NAME을 기준으로 선택할 수 있는 selectbox 생성
with col11:
    city_name = st.selectbox('CITY 선택', df_total['CITY'].unique())
    filtered_df_city = df_total[df_total['CITY'] == city_name].sort_values(by=['CITY'], axis=0)


with col12:
    entity_name = st.selectbox('은행 선택', filtered_df_city['ENTITY_NAME'].unique())
    filtered_df = filtered_df_city[filtered_df_city['ENTITY_NAME'] == entity_name].sort_values(by=['YEAR'], axis=0)
    
with col13:
    year_name = st.selectbox('연도 선택', filtered_df['YEAR'])
    filtered_year_df = filtered_df[filtered_df['YEAR'] == year_name].sort_values(by=['YEAR'], axis=0)

col21, col22 = st.columns([0.6, 0.4])

timeline_chart = alt.Chart( 
    filtered_df
    ).mark_area( 
        line={'color':'darkgreen'},
        interpolate='basis',
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='white', offset=0),
                alt.GradientStop(color='darkgreen', offset=1)
                ],
            x1=1,
            x2=1,
            y1=1,
            y2=0
            )
    ).encode( # https://altair-viz.github.io/user_guide/encodings/index.html#encoding-data-types
        x=alt.X('YEAR', title='', axis=alt.Axis(tickCount=20)),
        y=alt.Y('VALUE', title='구매 건 수')
    ).properties(
        height=300
    ).interactive()
col21.altair_chart(timeline_chart, use_container_width=True)



