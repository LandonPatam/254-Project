import streamlit as st
import random
from Home import *
prev_value = None



random_value = random.randint(1, count_items(conn))
while random_value == prev_value:
            random_value = random.randint(1, count_items(conn))
        
prev_value = random_value
study_value = get_word_by_id(conn, random_value)



st.metric(label = "Word", value = study_value[1], delta = study_value[4])

        # Declares 4 random ints
item_count = count_items(conn) 

        # Generate 4 unique random numbers in the range from 1 to count_items
random_numbers = random.sample(range(1, item_count + 1), 4)

        # Assign each random number to a separate variable
var1, var2, var3, var4 = random_numbers

print(study_value)


        # Create 4 columns
col1, col2, col3, col4 = st.columns(4)

        # Add buttons to each column
    
with col1:
    button1_label = get_definition(conn, var1)  # Get the definition only once
    if st.button(button1_label):  # Use the variable for the label
        if study_value[2] == button1_label:  # Compare the definition with the correct value
            st.write("Correct Definition")
        else:
            st.write("Wrong Definition")

with col2:
    button2_label = get_definition(conn, var2)  # Get the definition only once
    if st.button(button2_label):  # Use the variable for the label
        if study_value[2] == button2_label:
            st.write("Correct Definition")
        else:
            st.write("Wrong Definition")

with col3:
    button3_label = get_definition(conn, var3)  # Get the definition only once
    if st.button(button3_label):  # Use the variable for the label
        if study_value[2] == button3_label:  # Compare the definition with the correct value
            st.write("Correct Definition")
        else:
            st.write("Wrong Definition")

with col4:
    button4_label = get_definition(conn, var4)  # Get the definition only once
    if st.button(button4_label):  # Use the variable for the label
        if study_value[2] == button4_label:  # Compare the definition with the correct value
            st.write("Correct Definition")
        else:
            st.write("Wrong Definition")








