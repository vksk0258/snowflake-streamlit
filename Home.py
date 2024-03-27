import streamlit as st

st.set_page_config(page_icon="💬", page_title="Chat-Bot 🤖")

#Contact
with st.sidebar.expander("📬 Contact"):

    st.write("**GitHub:**")
    st.write("**Medium:** ")
    st.write("**Twitter:**")
    st.write("**Mail** :")



#Title
st.markdown(
    """
    <h2 style='text-align: center;'>Your data-aware assistant 🤖</h1>
    """,
    unsafe_allow_html=True,)

st.markdown("---")


#Description
st.markdown(
    """ 
    <h5 style='text-align:center;'>An intelligent chatbot created by combining 
    the strengths of Langchain and Streamlit. I use large language models to provide
    context-sensitive interactions. My goal is to help you better understand your data.
    I support PDF, TXT, CSV, Youtube transcript 🧠</h5>
    """,
    unsafe_allow_html=True)
st.markdown("---")