import sqlite3
import streamlit as st
import pandas as pd
import altair as alt
import random
import json

# DATABASE CONNECTIONS
conn = sqlite3.connect('vocabulary2.db', check_same_thread=False)
cursor = conn.cursor()

# CREATES TABLE
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vocabulary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL UNIQUE,
        definition TEXT NOT NULL,
        known TEXT NOT NULL DEFAULT 'unknown'
    )
''')
conn.commit()


# ADDED EXTRA COLUMN TO TABLE 
#cursor.execute('''
#    ALTER TABLE vocabulary
#    ADD COLUMN progress_tracker INTEGER DEFAULT 0
#''')
#conn.commit()


# TEST VARIABLES
my_dict = {
    'key1': ['value1_1', 'value1_2'],
    'key2': ['value2_1', 'value2_2'],
    'key3': ['value3_1', 'value3_2']
}

new_list = {}
completed_task_count = 0
print(completed_task_count)

# ADDS DATA TO TABLE
def add_data(conn, word, definition, learned):
    try:

        cur = conn.cursor()
        cur.execute(''' INSERT INTO vocabulary(word, definition, known) VALUES(?,?,?) ''',        (word, definition, learned)        )
        conn.commit()
        return True

    except sqlite3.Error:
        print("ALREADY IN DB")
        return False



def add_full_data(conn, word, defintion, learned, progress_tracker):
    try:

        cur = conn.cursor()
        cur.execute(''' INSERT INTO vocabulary(word, definition, known, progress_tracker) VALUES (?,?,?,?)  ''',      (word, defintion, learned, progress_tracker))
        conn.commit()

    except sqlite3.Error:
        print("ERROR ADDING FULL DATA VIA IMPORT")


# GETS DATA FROM TABLE 
def get_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM vocabulary")
    new_list = cur.fetchall()
    return new_list



#add_full_data(conn, "thing99", "thing99def", "known", "5")



# DELETES ALL DATA
def delete_data(conn):
    try:


        cur = conn.cursor()
        cur.execute("DELETE from vocabulary")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='vocabulary'")
        conn.commit()
    
    except sqlite3.Error:
        print("ERROR IN DELETING DB DATA")

# RETRIEVES WORD BY ID 
def get_word_by_id(conn, word_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM vocabulary WHERE id = ?", (word_id,))
    result = cur.fetchone()
    return result


# RETRIVES WORD BY ID AND KNOWN STATUS
def get_word_by_id_and_unknown(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM vocabulary WHERE known = ?", ("unknown",)) 
    result = cur.fetchall()
    return result


list = get_word_by_id_and_unknown(conn)
unknown_indexes = []
for i in list:
    unknown_indexes.append(i[0])

print(unknown_indexes)
    





# RETURNS COUNT OF ALL ITEMS IN TABLE
def count_items(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM vocabulary")
    count = cur.fetchone()[0] 
    return count

# INCREMENTS PROGRESS TRACKER VARIABLE
def increment_progress_tracker(conn, row_id, increment_value=1):
    try:
        
        cur = conn.cursor()
        cur.execute('''
            UPDATE vocabulary
            SET progress_tracker = progress_tracker + ?
            WHERE id = ?
        ''', (increment_value, row_id))
        conn.commit()
        print(f"Progress tracker for row id {row_id} updated successfully.")
    except sqlite3.Error:
        print(f"An error occurred")

# CHANGES STATUS OF WORD FROM UNKNOWN TO KNOWN
def mark_word_as_known(conn, row_id):
    try:
        
        cursor = conn.cursor()
        
        
        cursor.execute('''
            UPDATE vocabulary
            SET known = 'known'
            WHERE id = ?
        ''', (row_id,))
        
        
        conn.commit()
        print(f"Word with ID {row_id} is now marked as known.")
    
    except sqlite3.Error:
        print(f"An error occurred")


def mark_word_as_UNknown(conn, row_id):
    try:
        
        cursor = conn.cursor()
        
        
        cursor.execute('''
            UPDATE vocabulary
            SET known = 'unknown'
            WHERE id = ?
        ''', (row_id,))
        
        
        conn.commit()
        print(f"Word with ID {row_id} is now marked as known.")
    
    except sqlite3.Error:
        print(f"An error occurre")


# DECREMENTS PROGRESS TRACKER
def decrement_progress_tracker(conn, row_id, decrement_value=1):
    try:
        cur = conn.cursor()
        cur.execute('''
            UPDATE vocabulary
            SET progress_tracker = progress_tracker - ?
            WHERE id = ?
        ''', (decrement_value, row_id))
        conn.commit()
        print(f"Progress tracker for row id {row_id} decremented successfully.")
    except sqlite3.Error:
        print(f"An error occurred")

# RETRIEVES PROGRESS TRACKER
def get_progress_tracker(conn, row_id):
    try:
        cur = conn.cursor()
        cur.execute('''
            SELECT progress_tracker 
            FROM vocabulary 
            WHERE id = ?
        ''', (row_id,))
        result = cur.fetchone()
        if result:
            return result[0]  
        else:
            print(f"No entry found with id {row_id}.")
            return None
    except sqlite3.Error:
        print(f"An error occurred")
        return None
    
# RETRIEVES DEFINITIONS
def get_definition(conn, row_id):
    try:
        cur = conn.cursor()
        cur.execute('''
            SELECT definition
            FROM vocabulary
            WHERE id = ?
        ''', (row_id,))
        result = cur.fetchone()
        if result:
            return result[0]
    
    except sqlite3.Error:
        print("Error retrieving definition")
        return None



# MORE TEST SECTION

#print(get_random_definition(conn))
#delete_data(conn)
#add_data(conn, "thing", "thing_def", "unknown")
#increment_progress_tracker(conn, 1)
#decrement_progress_tracker(conn, 1)
#print(get_word_by_id(conn, 1))
#list = get_data(conn)
#for i in list: print (i)
#test_word = (get_word_by_id(conn, 4))
#print(test_word)
#print(test_word[2])


# DATA MANIPULATION

list = get_data(conn)
learned = 0
not_learned = 0

learned_data = []
for i in list:
    if i[3] == "known":
        learned += 1
    elif i[3] == "unknown":
        not_learned +=1
    if i[4] >= 5:
        mark_word_as_known(conn, i[0])
        print("NEW WORD LEARNED")
    elif i[4] < 5:
        mark_word_as_UNknown(conn, i[0])
        print("WORD UNLEARNED")

learned_data.append(learned)
learned_data.append(not_learned)






# STREAMLIT SECTION





# LIST OF WORDS

df = pd.DataFrame(list)
df.columns = ['ID', 'Word', 'Definition', 'Learned Status', 'Progress Counter']
st.title("Vocab words")
df = df.iloc[:, 1:]
st.table(df)



# EXPORT AS JSON BUTTON

if st.button("Generate JSON from data"):
    new_list = get_data(conn)
    with open("StudyWords.json", 'w') as json_file:
        json.dump(new_list, json_file, indent=4)
    st.write("Exported as JSON")



# BAR CHART
labels = ["Learned", "Not Learned"]
df = pd.DataFrame({'Learned Status': labels, 'Values': learned_data})
st.title("Known vs Unknown")
chart = alt.Chart(df).mark_bar(size=20).encode(
    x=alt.X('Learned Status', axis=alt.Axis(labelAngle=0)),

    y=alt.Y('Values')
)
st.altair_chart(chart, use_container_width=True)







#streamlit run test2.py
