import streamlit as st
import random
from Home import *
prev_value = None

if st.button("Start Studying"):
    try:
        random_value = random.randint(1, count_items(conn))
        while random_value == prev_value:
            random_value = random.randint(1, count_items(conn))
        
        prev_value = random_value
        value = get_word_by_id(conn, random_value)
        st.write(f"{value[1]}")
    except:
        st.header("No Values in Database")




