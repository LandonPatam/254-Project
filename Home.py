import sqlite3
import streamlit as st
import pandas as pd
import altair as alt
import random

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

# GETS DATA FROM TABLE 
def get_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM vocabulary")
    new_list = cur.fetchall()
    return new_list


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
    result = cur.fetchone()  # fetchone() returns a single record or None
    return result

# RETURNS COUNT OF ALL ITEMS IN TABLE
def count_items(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM vocabulary")
    count = cur.fetchone()[0]  # fetchone() returns a tuple (count,) so we access the first element
    return count

# INCREMENTS PROGRESS TRACKER VARIABLE
def increment_progress_tracker(conn, row_id, increment_value=1):
    try:
        # Update the progress_tracker for the specified row
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
        # Create a cursor to interact with the database
        cursor = conn.cursor()
        
        # Update the 'known' column to 'known' for the specific row
        cursor.execute('''
            UPDATE vocabulary
            SET known = 'known'
            WHERE id = ?
        ''', (row_id,))
        
        # Commit the changes to the database
        conn.commit()
        print(f"Word with ID {row_id} is now marked as known.")
    
    except sqlite3.Error:
        print(f"An error occurred")


def mark_word_as_UNknown(conn, row_id):
    try:
        # Create a cursor to interact with the database
        cursor = conn.cursor()
        
        # Update the 'known' column to 'known' for the specific row
        cursor.execute('''
            UPDATE vocabulary
            SET known = 'unknown'
            WHERE id = ?
        ''', (row_id,))
        
        # Commit the changes to the database
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
            return result[0]  # Fetch the progress_tracker value
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

#Creates labels for the bars
labels = ["Learned", "Not Learned"]

# Create a DataFrame for better visualization
df = pd.DataFrame({'Learned Status': labels, 'Values': learned_data})

# Set the title of the app
st.title("Known vs Unknown")


# Create an Altair bar chart with thinner bars
chart = alt.Chart(df).mark_bar(size=20).encode(
    x=alt.X('Learned Status', axis=alt.Axis(labelAngle=0)),  # Set label angle to 0 for horizontal labels

    y=alt.Y('Values')
)




# Display the chart
st.altair_chart(chart, use_container_width=True)

# Populate with data
df = pd.DataFrame(list)

# Set the title of the app
st.title("Vocab words")

# Rename the columns if desired
df = df.iloc[:, 1:]

# Display the DataFrame as a table with new headers
st.table(df)


#streamlit run test2.py
