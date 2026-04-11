import streamlit as st
import pandas as pd
import pygwalker as pyg
from sqlalchemy import create_engine, inspect

st.set_page_config(layout="wide")
st.title("AI Data Explorer + SQL (Kanaries Graphic Walker)")

# session state
if "df" not in st.session_state:
    st.session_state.df = None

if "engine" not in st.session_state:
    st.session_state.engine = None

tab1, tab2, tab3 = st.tabs(["Upload CSV", "Connect SQL", "Visualization"])

# ===============================
# TAB 1 — Upload CSV
# ===============================
with tab1:
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        st.session_state.df = pd.read_csv(file)
        st.success("CSV Loaded")
        st.dataframe(st.session_state.df.head())

# ===============================
# TAB 2 — SQL CONNECTION
# ===============================
with tab2:
    st.subheader("Connect to Database")

    db_type = st.selectbox("Database Type",
        ["SQLite", "PostgreSQL", "MySQL", "SQL Server"]
    )

    conn_string = st.text_input(
        "Connection String",
        placeholder="Examples:\n"
        "SQLite: sqlite:///mydb.db\n"
        "Postgres: postgresql://user:pass@host:5432/db\n"
        "MySQL: mysql+pymysql://user:pass@host/db\n"
        "SQL Server: mssql+pyodbc://user:pass@dsn"
    )

    if st.button("Connect"):
        try:
            engine = create_engine(conn_string)
            st.session_state.engine = engine
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            st.session_state.tables = tables
            st.success("Connected successfully!")
        except Exception as e:
            st.error(str(e))

    # Choose table
    if st.session_state.engine:
        table = st.selectbox("Select Table", st.session_state.tables)

        if st.button("Load Table"):
            query = f"SELECT * FROM {table}"
            st.session_state.df = pd.read_sql(query, st.session_state.engine)
            st.success("Table loaded!")
            st.dataframe(st.session_state.df.head())

# ===============================
# TAB 3 — KANARIES VISUALIZATION
# ===============================
with tab3:
    if st.session_state.df is None:
        st.warning("Upload CSV or load SQL table first.")
    else:
        st.write("Drag & Drop fields to explore 👇")

        pyg_html = pyg.walk(st.session_state.df, return_html=True)
        st.components.v1.html(pyg_html, height=900, scrolling=True)