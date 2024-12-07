import streamlit as st
from Home import *


st.title("Upload a File")

uploaded_file = st.file_uploader("Import data via a JSON file", type=["json"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")
   
    st.write(f"File name: {uploaded_file.name}")
    raw_json = uploaded_file.read() 
    decoded_json = raw_json.decode("utf-8")

    json_as_list = json.loads(decoded_json)
    delete_data(conn)
    for i in json_as_list:
        add_full_data(conn, i[1], i[2], i[3], i[4])


    

