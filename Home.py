import sqlite3
import streamlit as st
import pandas as pd
import altair as alt
import random

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('vocabulary2.db', check_same_thread=False)

# Create a cursor
cursor = conn.cursor()

# Create the vocabulary table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vocabulary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL UNIQUE,
        definition TEXT NOT NULL,
        known TEXT NOT NULL DEFAULT 'unknown'
    )
''')
conn.commit()



#cursor.execute('''
#    ALTER TABLE vocabulary
#    ADD COLUMN progress_tracker INTEGER DEFAULT 0
#''')

#conn.commit()

my_dict = {
    'key1': ['value1_1', 'value1_2'],
    'key2': ['value2_1', 'value2_2'],
    'key3': ['value3_1', 'value3_2']
}

new_list = {}



def add_data(conn, word, definition, learned):
    try:

        cur = conn.cursor()
        cur.execute(''' INSERT INTO vocabulary(word, definition, known) VALUES(?,?,?) ''',        (word, definition, learned)        )
        conn.commit()
        return True

    except sqlite3.Error:
        print("ALREADY IN DB")
        return False

def get_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM vocabulary")
    new_list = cur.fetchall()
    return new_list

def delete_data(conn):
    try:


        cur = conn.cursor()
        cur.execute("DELETE from vocabulary")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='vocabulary'")
        conn.commit()
    
    except sqlite3.Error:
        print("ERROR IN DELETING DB DATA")


def get_word_by_id(conn, word_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM vocabulary WHERE id = ?", (word_id,))
    result = cur.fetchone()  # fetchone() returns a single record or None
    return result


def count_items(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM vocabulary")
    count = cur.fetchone()[0]  # fetchone() returns a tuple (count,) so we access the first element
    return count

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



#print(get_random_definition(conn))
#delete_data(conn)
#add_data(conn, "thing", "thing_def", "unknown")
#increment_progress_tracker(conn, 1)
#decrement_progress_tracker(conn, 1)
#print(get_word_by_id(conn, 1))
#list = get_data(conn)
#for i in list: print (i)
test_word = (get_word_by_id(conn, 4))
print(test_word)
print(test_word[2])



list = get_data(conn)
learned = 0
not_learned = 0

learned_data = []
for i in list:
    if i[3] == "known":
        learned += 1
    elif i[3] == "unknown":
        not_learned +=1

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
