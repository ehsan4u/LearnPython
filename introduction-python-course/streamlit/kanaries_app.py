# pip install pygwalker streamlit

import streamlit as st
import pandas as pd
import pygwalker as pyg

st.set_page_config(layout="wide")
st.title("AI Data Explorer (Kanaries Graphic Walker)")

tab1, tab2 = st.tabs(["Data", "Visualization"])

if "df" not in st.session_state:
    st.session_state.df = None

# ---------------- DATA TAB ----------------
with tab1:
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        st.session_state.df = pd.read_csv(uploaded_file)

    if st.session_state.df is not None:
        st.dataframe(st.session_state.df)
        st.write(st.session_state.df.describe())

# ---------------- VISUALIZATION TAB ----------------
with tab2:
    if st.session_state.df is None:
        st.warning("Upload dataset first.")
    else:
        st.write("Drag & drop fields like Tableau 👇")

        pyg_html = pyg.walk(st.session_state.df, return_html=True)
        st.components.v1.html(pyg_html, height=900, scrolling=True)