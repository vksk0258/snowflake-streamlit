from openai import OpenAI
import re
import streamlit as st
from prompts import get_system_prompt
import pandas as pd

from dotenv import load_dotenv
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI as ai
import os

load_dotenv()
OpenAI.api_key = st.secrets.OPENAI_API_KEY
llm = ai(api_token=OpenAI.api_key)

