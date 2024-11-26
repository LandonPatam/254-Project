import streamlit as st
from Home import *
import sqlite3




# Session for Page1
if "word" not in st.session_state:
    st.session_state.word = ""
if "definition" not in st.session_state:
    st.session_state.definition = ""


word = st.text_input("Enter your vocab word", value=st.session_state.word, key="word")
definition = st.text_input("Enter the definition", value=st.session_state.definition, key="definition")
learned = "unknown"


if st.button("Submit"):
    if word and definition:
        add_data(conn, word, definition, learned)


if st.button("Delete all data"):
    delete_data(conn)



