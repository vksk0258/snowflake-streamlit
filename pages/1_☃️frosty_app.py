from openai import OpenAI
import re
import streamlit as st
from prompts import get_system_prompt
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI as ai
from dotenv import load_dotenv
import os


load_dotenv()
#secrets.toml 파일로 api키 호출
llm = ai(api_token=st.secrets.OPENAI_API_KEY)
client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)
st.title("☃️ Frosty")

# 채팅 메시지 기록 초기화
if "messages" not in st.session_state:
    # system prompt includes table information, rules, and prompts the LLM to produce
    # a welcome message to the user.
    st.session_state.messages = [{"role": "system", "content": get_system_prompt()}]

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

# display the existing chat messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "results" in message:
            st.dataframe(message["results"])

# If last message is not from assistant, we need to generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = ""
        resp_container = st.empty()
        for delta in client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        ):
            response += (delta.choices[0].delta.content or "")
            resp_container.markdown(response)

        message = {"role": "assistant", "content": response}
        # Parse the response for a SQL query and execute if available
        sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)
        if sql_match:
            sql = sql_match.group(1)
            conn = st.connection("snowflake")
            message["results"] = conn.query(sql)
            st.dataframe(message["results"])
            
            df = pd.DataFrame(message["results"])
            sdf = SmartDataframe(df,config={"llm":llm})
            response=sdf.chat(prompt)
            st.image('D:/Snowflake/streamlit/snowflake-streamlit/exports/charts/temp_chart.png')
        st.session_state.messages.append(message)
