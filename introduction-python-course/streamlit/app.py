# pip install streamlit pandas plotly
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data & Visualization App", layout="wide")

st.title("Data and Visualization Dashboard")

# --- Tabs ---
tab1, tab2 = st.tabs(["📊 Data", "📈 Visualization"])

# --- Session state to keep data ---
if "df" not in st.session_state:
    st.session_state.df = None

# =========================
# TAB 1 — DATA
# =========================
with tab1:
    st.header("Upload or View Data")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        st.session_state.df = pd.read_csv(uploaded_file)

    if st.session_state.df is not None:
        st.subheader("Dataset Preview")
        st.dataframe(st.session_state.df, use_container_width=True)

        st.subheader("Dataset Info")
        st.write(st.session_state.df.describe())

# =========================
# TAB 2 — VISUALIZATION
# =========================
with tab2:
    st.header("Build Visualization")

    df = st.session_state.df

    if df is None:
        st.warning("Upload data first in the Data tab.")
    else:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        all_cols = df.columns.tolist()

        chart_type = st.selectbox(
            "Select Chart Type",
            ["Scatter", "Line", "Bar", "Histogram", "Box"]
        )

        x_axis = st.selectbox("X-Axis", all_cols)
        y_axis = st.selectbox("Y-Axis", numeric_cols)

        color = st.selectbox("Color (optional)", [None] + all_cols)

        # --- Create chart ---
        if chart_type == "Scatter":
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color)
        elif chart_type == "Line":
            fig = px.line(df, x=x_axis, y=y_axis, color=color)
        elif chart_type == "Bar":
            fig = px.bar(df, x=x_axis, y=y_axis, color=color)
        elif chart_type == "Histogram":
            fig = px.histogram(df, x=x_axis, color=color)
        elif chart_type == "Box":
            fig = px.box(df, x=x_axis, y=y_axis, color=color)

        st.plotly_chart(fig, use_container_width=True)