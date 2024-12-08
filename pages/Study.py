import streamlit as st
import random
from Home import *




# INITIALIZES SESSION STATE AND SETS ALL VARIABLES FOR SESSION


if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = None


study_set = ""
list = get_word_by_id_and_unknown(conn)
#print(list)
unknown_indexes = []
for i in list:
    unknown_indexes.append(i[0])
#print(unknown_indexes)

# BUTTONS FOR FILTERS
col1, col2 = st.columns(2)


with col1:
    if st.button("ALL WORDS"):
        st.session_state.button_clicked = "ALL WORDS"
        st.session_state.study_set = "ALL WORDS"
        study_set = "ALL WORDS"
        item_count = count_items(conn) 
        random_numbers = random.sample(range(1, item_count + 1), 4)
        var1, var2, var3, var4 = random_numbers
        st.session_state.var1 = var1
        st.session_state.var2 = var2
        st.session_state.var3 = var3
        st.session_state.var4 = var4


with col2:
    if st.button("UNKNOWN WORDS"):
        try:
            st.session_state.button_clicked = "UNKNOWN WORDS"
            st.session_state.study_set = "UNKNOWN WORDS" 
            study_set = "UNKNOWN WORDS"

            
            random_numbers = random.sample(unknown_indexes, 4)
            var1, var2, var3, var4 = random_numbers
            #print(var1)
            #print(var2)
            #print(var3)
            #print(var4)
            st.session_state.var1 = var1
            st.session_state.var2 = var2
            st.session_state.var3 = var3
            st.session_state.var4 = var4
        except:
            st.write("NOT ENOUGH WORDS IN VOCAB LIST")



if st.session_state.button_clicked is None:
    st.stop()



list = get_data(conn)

previous_word = ""


if len(list) >= 4:
    if 'study_value' not in st.session_state:
        if study_set == "ALL WORDS":
            random_value = random.randint(1, count_items(conn))
        elif study_set == "UNKNOWN WORDS":
            random_value = random.choice(unknown_indexes) 
        study_value = get_word_by_id(conn, random_value)
        st.session_state.study_value = study_value
        previous_word = study_value


        # GETS RANDOM INDEX AND ASSIGNS FROM ALL INDEXES
        #if st.button("ALL WORDS"):
        #    item_count = count_items(conn) 
        #    random_numbers = random.sample(range(1, item_count + 1), 4)
        #    var1, var2, var3, var4 = random_numbers



        # GETS RANDOM INDEX AND ASSIGNS FROM UNKNOWN INDEXES
        #if st.button("UNKNOWN WORDS"):
        ##    list = get_word_by_id_and_unknown(conn)
        #  unknown_indexes = []
        #    for i in list:
        #        unknown_indexes.append(i[0])
        #    random_numbers = random.sample(unknown_indexes, 4)
        #    var1, var2, var3, var4 = random_numbers


        #list = get_word_by_id_and_unknown(conn)

        #st.session_state.var1 = var1
        #st.session_state.var2 = var2
        #st.session_state.var3 = var3
        #st.session_state.var4 = var4


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



    # DISPLAYS CURRENT WORD / METRICS OF WORD
    st.metric(label="Word", value=st.session_state.study_value[1], delta=st.session_state.study_value[4])


    # CREATES COLUMNS FOR THE DEFINITION BUTTONS AND MAKES THE BUTTONS
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        button1_label = get_definition(conn, st.session_state.var1)
        if st.button(button1_label):
            if st.session_state.study_value[2] == button1_label:
                st.write("Correct Definition")
                increment_progress_tracker(conn, st.session_state.study_value[0])

            else:
                st.write("Wrong Definition")
                decrement_progress_tracker(conn, st.session_state.study_value[0])


    with col2:
        button2_label = get_definition(conn, st.session_state.var2)
        if st.button(button2_label):
            if st.session_state.study_value[2] == button2_label:
                st.write("Correct Definition")
                increment_progress_tracker(conn, st.session_state.study_value[0])

            else:
                st.write("Wrong Definition")
                decrement_progress_tracker(conn, st.session_state.study_value[0])


    with col3:
        button3_label = get_definition(conn, st.session_state.var3)
        if st.button(button3_label):
            if st.session_state.study_value[2] == button3_label:
                st.write("Correct Definition")
                increment_progress_tracker(conn, st.session_state.study_value[0])

            else:
                st.write("Wrong Definition")
                decrement_progress_tracker(conn, st.session_state.study_value[0])

    with col4:
        button4_label = get_definition(conn, st.session_state.var4)
        if st.button(button4_label):
            if st.session_state.study_value[2] == button4_label:
                st.write("Correct Definition")
                increment_progress_tracker(conn, st.session_state.study_value[0])
            else:
                st.write("Wrong Definition")
                decrement_progress_tracker(conn, st.session_state.study_value[0])

    # NEXT WORD BUTTON FOR RANDOMIZING NEXT WORD / BUTTON DEFINITIONS
    if st.button("Next Word"):
        if study_set == "ALL WORDS" or st.session_state.study_set == "ALL WORDS":
            random_value = random.randint(1, count_items(conn))
        elif study_set == "UNKNOWN WORDS" or st.session_state.study_set == "UNKNOWN WORDS":
            random_value = random.choice(unknown_indexes) 
        study_value = get_word_by_id(conn, random_value)
        st.session_state.study_value = study_value  


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



        st.rerun() 
