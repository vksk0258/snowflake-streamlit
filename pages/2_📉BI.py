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
df_Insured = df[df['VARIABLE_NAME'].str.contains('Total deposits')]

col11, col12, col13, col14 = st.columns([0.25, 0.25, 0.25, 0.25])

# with col11:
#     state_name_options = np.sort(df_total['STATE_ABBREVIATION'].unique())
#     state_name = st.selectbox('SELECT STATE CODE', state_name_options)
#     filtered_df_state = df_total[df_total['STATE_ABBREVIATION'] == state_name]

#     state_name_options_Insured = np.sort(df_Insured['STATE_ABBREVIATION'].unique())
#     filtered_df_state_Insured = df_Insured[df_Insured['STATE_ABBREVIATION'] == state_name]

#     # st.dataframe(filtered_df_state_Insured)


# # ENTITY_NAME을 기준으로 선택할 수 있는 selectbox 생성
# with col12:
#     city_name_options = np.sort(filtered_df_state['CITY'].unique())
#     city_name = st.selectbox('SELECT CITY', city_name_options)
#     filtered_df_city = filtered_df_state[filtered_df_state['CITY'] == city_name]

#     city_name_options_Insured = np.sort(filtered_df_state_Insured['CITY'].unique())
#     filtered_df_city_Insured = filtered_df_state_Insured[filtered_df_state_Insured['CITY'] == city_name]

#     # st.dataframe(filtered_df_state_Insured)


# with col13:
#     entity_name_options = np.sort(filtered_df_city['ENTITY_NAME'].unique())
#     entity_name = st.selectbox('SELECT BANK', entity_name_options)
#     filtered_df = filtered_df_city[filtered_df_city['ENTITY_NAME'] == entity_name]

#     entity_name_options_Insured = np.sort(filtered_df_city_Insured['ENTITY_NAME'].unique())
#     filtered_df_Insured = filtered_df_city_Insured[filtered_df_city_Insured['ENTITY_NAME'] == entity_name]

#     # st.dataframe(filtered_df_Insured)

# with col14:
#     # unique()로 얻은 연도를 np.sort()를 사용하여 정렬합니다.
#     year_options = np.sort(filtered_df_city['YEAR'].unique())
#     year_name = st.selectbox('SELECT YEAR', year_options)
#     filtered_year_df = filtered_df_city[filtered_df_city['YEAR'] == year_name]

#     year_options_Insured = np.sort(filtered_df_city_Insured['YEAR'].unique())
#     filtered_year_df_Insured = filtered_df_city_Insured[filtered_df_city_Insured['YEAR'] == year_name]



state_name_options = np.sort(df_total['STATE_ABBREVIATION'].unique())
state_name = st.sidebar.selectbox('SELECT STATE CODE', state_name_options)
filtered_df_state = df_total[df_total['STATE_ABBREVIATION'] == state_name]

state_name_options_Insured = np.sort(df_Insured['STATE_ABBREVIATION'].unique())
filtered_df_state_Insured = df_Insured[df_Insured['STATE_ABBREVIATION'] == state_name]

city_name_options = np.sort(filtered_df_state['CITY'].unique())
city_name = st.sidebar.selectbox('SELECT CITY', city_name_options)
filtered_df_city = filtered_df_state[filtered_df_state['CITY'] == city_name]

city_name_options_Insured = np.sort(filtered_df_state_Insured['CITY'].unique())
filtered_df_city_Insured = filtered_df_state_Insured[filtered_df_state_Insured['CITY'] == city_name]

entity_name_options = np.sort(filtered_df_city['ENTITY_NAME'].unique())
entity_name = st.sidebar.selectbox('SELECT BANK', entity_name_options)
filtered_df = filtered_df_city[filtered_df_city['ENTITY_NAME'] == entity_name]

entity_name_options_Insured = np.sort(filtered_df_city_Insured['ENTITY_NAME'].unique())
filtered_df_Insured = filtered_df_city_Insured[filtered_df_city_Insured['ENTITY_NAME'] == entity_name]

year_options = np.sort(filtered_df_city['YEAR'].unique())
year_name = st.sidebar.selectbox('SELECT YEAR', year_options)
filtered_year_df = filtered_df_city[filtered_df_city['YEAR'] == year_name]

year_options_Insured = np.sort(filtered_df_city_Insured['YEAR'].unique())
filtered_year_df_Insured = filtered_df_city_Insured[filtered_df_city_Insured['YEAR'] == year_name]


st.divider()

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
        y=alt.Y('VALUE', title='총 자산')
    ).properties(
        height=300,
        title= entity_name+" Annual Total Asset Graph"
    ).interactive()
col21.subheader(entity_name+"은행 연도별 총 자산 추이", divider='green')
col21.altair_chart(timeline_chart, use_container_width=True)


color_scale = alt.Scale(scheme='greens', reverse=True)
pie_chart = (
    alt.Chart(filtered_year_df)
    .mark_arc()
    .encode(
        theta=alt.Theta('VALUE'),
        color=alt.Color('ENTITY_NAME', scale=color_scale, sort=["VALUE"])
    )
).properties(
    width=300,
    height=300
)
col22.subheader(str(year_name)+"년도 "+city_name+" 자산 비율", divider='green')
col22.altair_chart(pie_chart, use_container_width=True)


# 기존 파이 차트 생성 코드
# color_scale = alt.Scale(scheme='greens', reverse=True)
# pie_chart = alt.Chart(filtered_year_df).mark_arc().encode(
#     theta=alt.Theta('VALUE:Q'),
#     color=alt.Color('ENTITY_NAME:N', scale=color_scale, sort=["VALUE"])
# ).properties(
#     width=300,
#     height=300,
#     title=str(year_name)+"년도 "+city_name+"의 은행 자산 비율"
# )

# # 텍스트 레이어 추가
# text = pie_chart.mark_text(radiusOffset=10, align='center', baseline='middle').encode(
#     text=alt.Text('VALUE:Q'),  # 여기서 'Q'는 양적 데이터를 의미
#     theta=alt.Theta('VALUE:Q')
# )

# # 파이 차트와 텍스트 레이어 결합
# final_chart = pie_chart + text

# # 스트림릿에 차트 표시 (스트림릿을 사용하는 경우)

# pie_chart = alt.Chart(filtered_year_df).mark_arc(innerRadius=0, outerRadius=100).encode(
#     theta=alt.Theta(field='VALUE', type='quantitative', stack=True),  # 각도를 값으로 설정
#     color=alt.Color('ENTITY_NAME:N', scale=color_scale, sort=["VALUE"]),
# ).properties(
#     width=300,
#     height=300,
#     title=str(year_name)+"년도 "+city_name+"의 은행 자산 비율"
# )

# # 텍스트 레이어 추가 - 각 파이 조각 위에 값 표시
# text_layer = pie_chart.mark_text(radius=80,  # 텍스트 위치 조정 (원의 중심에서 50% 더 떨어진 위치)
#                                  align='center',
#                                  baseline='middle',
#                                  angle=0).encode(
#     text='VALUE:Q',  # 표시할 텍스트 (값)
#     color=alt.value('blue'),
#     theta=alt.Theta(field='VALUE', type='quantitative', stack=True)  # 텍스트의 각도 조정
# )

# # 파이 차트와 텍스트 레이어 결합
# final_chart = pie_chart + text_layer
# col22.altair_chart(final_chart, use_container_width=True)

col31, col32 = st.columns([0.6, 0.4])

color_scale = alt.Scale(scheme='greens')
chart_top10 = (
    alt.Chart(filtered_year_df_Insured.sort_values(by='VALUE', ascending=False).head(5))
    .mark_bar()
    .encode(
        x=alt.X("VALUE", title="Deposit"),
        y=alt.Y("ENTITY_NAME", title="").sort('-x'),
        color=alt.Color("VALUE", scale=color_scale, legend=None),
    )
    .properties(height=240)
)

col32.subheader(city_name+" 예금 자산 순위", divider='green')
col32.altair_chart(chart_top10, theme="streamlit", use_container_width=True)