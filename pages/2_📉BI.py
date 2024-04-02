import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
from prompts import asset_desc, deposits_desc, loan_desc

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
df_deposits = df[df['VARIABLE_NAME'].str.contains('Total deposits')]
df_loan = df[df['VARIABLE_NAME'].str.contains('Loans')]


### 사이드바 ###
st.sidebar.title("USA FINANCE DASHBOARD📉")

st.sidebar.divider()

state_name_options = np.sort(df_total['STATE_ABBREVIATION'].unique())
state_name = st.sidebar.selectbox('SELECT STATE CODE', state_name_options)
filtered_df_state = df_total[df_total['STATE_ABBREVIATION'] == state_name]

state_name_options_Insured = np.sort(df_deposits['STATE_ABBREVIATION'].unique())
filtered_df_state_Insured = df_deposits[df_deposits['STATE_ABBREVIATION'] == state_name]
#####

city_name_options = np.sort(filtered_df_state['CITY'].unique())
city_name = st.sidebar.selectbox('SELECT CITY', city_name_options)
filtered_df_city = filtered_df_state[filtered_df_state['CITY'] == city_name]

city_name_options_Insured = np.sort(filtered_df_state_Insured['CITY'].unique())
filtered_df_city_Insured = filtered_df_state_Insured[filtered_df_state_Insured['CITY'] == city_name]

#####

entity_name_options = np.sort(filtered_df_city['ENTITY_NAME'].unique())
entity_name = st.sidebar.selectbox('SELECT BANK', entity_name_options)
filtered_df = filtered_df_city[filtered_df_city['ENTITY_NAME'] == entity_name]

entity_name_options_Insured = np.sort(filtered_df_city_Insured['ENTITY_NAME'].unique())
filtered_df_deposits = filtered_df_city_Insured[filtered_df_city_Insured['ENTITY_NAME'] == entity_name]

####

year_options = np.sort(filtered_df['YEAR'].unique())
year_name = st.sidebar.selectbox('SELECT YEAR', year_options)
filtered_year_df = filtered_df[filtered_df['YEAR'] == year_name]

year_options_Insured = np.sort(filtered_df_city_Insured['YEAR'].unique())
filtered_year_df_deposits = filtered_df_city_Insured[filtered_df_city_Insured['YEAR'] == year_name]

####

pre_filtered_year_df = filtered_df_city[filtered_df_city['YEAR'] == year_name-1]
pre_filtered_year_df_deposits = filtered_df_city_Insured[filtered_df_city_Insured['YEAR'] == year_name-1]

def calculate_percentage_change(current_value, previous_value):
    if previous_value == 0:
        return "최초년도 입니다"
    percentage_change = ((current_value - previous_value) / previous_value) * 100
    return f"{percentage_change:.2f}%"

col11, col12, col13 = st.columns(3)

#total asset 전년대 대비 비교
current_value = int(df_total.loc[(df_total['STATE_ABBREVIATION'] == state_name) & (df_total['CITY'] == city_name) & (df_total['YEAR'] == year_name) &(df_total['ENTITY_NAME']==entity_name), 'VALUE'])
try:
    previous_value = int(df_total.loc[(df_total['STATE_ABBREVIATION'] == state_name) & (df_total['CITY'] == city_name) & (df_total['YEAR'] == year_name-1) &(df_total['ENTITY_NAME']==entity_name), 'VALUE'])
except:
    previous_value = 0

col11.metric("총 자산(작년대비 등락률)", f'$ {current_value:,}', f'{calculate_percentage_change(current_value, previous_value)}',help=asset_desc) 


#deposit 전년도 대비 비교
current_value = int(filtered_year_df_deposits[filtered_year_df_deposits['ENTITY_NAME']==entity_name]['VALUE'].iloc[0])
try:
    previous_value = int(pre_filtered_year_df_deposits[pre_filtered_year_df_deposits['ENTITY_NAME']==entity_name]['VALUE'].iloc[0])
except:
    previous_value = 0

col12.metric("총 예금(작년대비 등락률)", f'$ {current_value:,}', f'{calculate_percentage_change(current_value, previous_value)}',help=deposits_desc) 

current_value = int(df_loan.loc[(df_loan['STATE_ABBREVIATION'] == state_name) & (df_loan['CITY'] == city_name) & (df_loan['YEAR'] == year_name) &(df_loan['ENTITY_NAME']==entity_name), 'VALUE'])

try:
    previous_value = int(df_loan.loc[(df_loan['STATE_ABBREVIATION'] == state_name) & (df_loan['CITY'] == city_name) & (df_loan['YEAR'] == year_name-1) &(df_loan['ENTITY_NAME']==entity_name), 'VALUE'])
except:
    previous_value = 0

col13.metric("총 대출금(작년대비 등락률)", f'$ {current_value:,}', f'{calculate_percentage_change(current_value, previous_value)}',help=loan_desc) 

st.divider()

col21, col22 = st.columns([0.9, 0.1])

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
col21.subheader(entity_name+" 연도별 총 자산 추이", divider='green')
col21.altair_chart(timeline_chart, use_container_width=True)

col31,exp1, col32 ,exp2 = st.columns([0.4,0.1,0.4,0.1])

color_scale = alt.Scale(scheme='greens', reverse=True)
pie_chart = (
    alt.Chart(df_total[(df_total['STATE_ABBREVIATION'] == state_name) & (df_total['CITY'] == city_name) & (df_total['YEAR'] == year_name)])
    .mark_arc()
    .encode(
        theta=alt.Theta('VALUE'),
        color=alt.Color('ENTITY_NAME', scale=color_scale, sort=["VALUE"])
    )
).properties(
    width=300,
    height=300
)
col31.subheader(str(year_name)+"년도 "+city_name+" 자산 비율", divider='green')
col31.altair_chart(pie_chart, use_container_width=True)


color_scale = alt.Scale(scheme='greens')
chart_top10 = (
    alt.Chart(filtered_year_df_deposits.sort_values(by='VALUE', ascending=False).head(10))
    .mark_bar()
    .encode(
        x=alt.X("VALUE", title="Deposit"),
        y=alt.Y("ENTITY_NAME", title="").sort('-x'),
        color=alt.Color("VALUE", scale=color_scale, legend=None),
    )
    .properties(height=300)
)

col32.subheader(city_name+" 예금 자산 순위", divider='green')
col32.altair_chart(chart_top10, theme="streamlit", use_container_width=True)

##### 맵생성
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

# Choropleth map
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(df_selected_year.population)),
                               scope="usa",
                               labels={'population':'Population'}
                              )
    choropleth.update_layout(
        # template='plotly_white',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth

df_reshaped = pd.read_csv('data/us-population-2010-2019-reshaped.csv')
df_selected_year = df_reshaped[df_reshaped.year == 2014]
df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)


col41, col42, ex1 = st.columns([0.6, 0.4, 0.1])

with col41:
    st.subheader("USA 인구밀집도", divider='green')
    choropleth = make_choropleth(df_selected_year, 'states_code', 'population', 'greens')
    st.plotly_chart(choropleth, use_container_width=True)
    
    heatmap = make_heatmap(df_reshaped, 'year', 'states', 'population', 'greens')
    st.altair_chart(heatmap, use_container_width=True)

with col42:

    st.subheader("인구수 테이블", divider='green')
    choropleth = make_choropleth(df_selected_year, 'states_code', 'population', 'greens')
    st.dataframe(df_selected_year_sorted,
                    column_order=("states", "population"),
                    hide_index=True,
                    width=None,
                    column_config={
                    "states": st.column_config.TextColumn(
                        "States",
                    ),
                    "population": st.column_config.ProgressColumn(
                        "Population",
                        format="%f",
                        min_value=0,
                        max_value=max(df_selected_year_sorted.population),
                        )}
                    )
