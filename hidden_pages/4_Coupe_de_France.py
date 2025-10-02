import streamlit as st
import pandas as pd
from sshtunnel import SSHTunnelForwarder
import pymysql
import time

st.title("Coupe de France")


query = "SHOW TABLES"
df = st.session_state.db_connection.query(query)
st.dataframe(df)

