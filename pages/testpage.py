import streamlit as st
import random
from Home import *



# Initialize session state for keeping track of current word
if 'study_value' not in st.session_state:
    random_value = random.randint(1, count_items(conn))
    study_value = get_word_by_id(conn, random_value)
    st.session_state.study_value = study_value  # Store it in session state


    item_count = count_items(conn) 
    random_numbers = random.sample(range(1, item_count + 1), 4)
    var1, var2, var3, var4 = random_numbers

    st.session_state.var1 = var1
    st.session_state.var2 = var2
    st.session_state.var3 = var3
    st.session_state.var4 = var4

# Show the current word
st.metric(label="Word", value=st.session_state.study_value[1], delta=st.session_state.study_value[4])


# Create 4 columns for the buttons
col1, col2, col3, col4 = st.columns(4)

# Add buttons to each column
with col1:
    button1_label = get_definition(conn, st.session_state.var1)  # Get the definition only once
    if st.button(button1_label):  # Use the variable for the label
        if st.session_state.study_value[2] == button1_label:  # Compare the definition with the correct value
            st.write("Correct Definition")
        else:
            st.write("Wrong Definition")

with col2:
    button2_label = get_definition(conn, st.session_state.var2)
    if st.button(button2_label):
        if st.session_state.study_value[2] == button2_label:
            st.write("Correct Definition")
        else:
            st.write("Wrong Definition")

with col3:
    button3_label = get_definition(conn, st.session_state.var3)
    if st.button(button3_label):
        if st.session_state.study_value[2] == button3_label:
            st.write("Correct Definition")
        else:
            st.write("Wrong Definition")

with col4:
    button4_label = get_definition(conn, st.session_state.var4)
    if st.button(button4_label):
        if st.session_state.study_value[2] == button4_label:
            st.write("Correct Definition")
        else:
            st.write("Wrong Definition")

# Add "Next Word" button to get a new word and update the session state
if st.button("Next Word"):
    random_value = random.randint(1, count_items(conn))
    study_value = get_word_by_id(conn, random_value)
    st.session_state.study_value = study_value  # Update the session state with the new word


    item_count = count_items(conn) 
    random_numbers = random.sample(range(1, item_count + 1), 4)
    var1, var2, var3, var4 = random_numbers
    st.session_state.var1 = var1
    st.session_state.var2 = var2
    st.session_state.var3 = var3
    st.session_state.var4 = var4

    if var1 != study_value[0] and var2 != study_value[0] and var3 != study_value[0] and var4 != study_value[0]:
        random_realanswer = random.randint(1, 4)
        if random_realanswer == 1:
            st.session_state.var1 = study_value[0]
        elif random_realanswer == 2:
            st.session_state.var2 = study_value[0]
        elif random_realanswer == 3:
            st.session_state.var3 = study_value[0]
        elif random_realanswer == 4:
            st.session_state.var4 = study_value[0]



    st.rerun()  # This reruns the app to update the displayed word
