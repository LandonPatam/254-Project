import sqlite3
import streamlit as st
import pandas as pd
import altair as alt

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('vocabulary2.db')

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


my_dict = {
    'key1': ['value1_1', 'value1_2'],
    'key2': ['value2_1', 'value2_2'],
    'key3': ['value3_1', 'value3_2']
}

new_list = {}



def add_data(conn, word, definition, learned):
    cur = conn.cursor()
    cur.execute(''' INSERT INTO vocabulary(word, definition, known) VALUES(?,?,?) ''',        (word, definition, learned)        )
    conn.commit()

def get_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM vocabulary")
    new_list = cur.fetchall()
    return new_list

def delete_data(conn):
    cur = conn.cursor()
    cur.execute("DELETE from vocabulary")
    conn.commit()


#add_data(conn, "thing5" , "thing5 def", "unknown")


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



# Sample data: List of values

# Optional: Create labels for the bars
labels = ["Learned", "Not Learned"]

# Create a DataFrame for better visualization
df = pd.DataFrame({'Learned Status': labels, '#': learned_data})

# Set the title of the app
st.title("Bar Chart Example")


# Create an Altair bar chart with thinner bars
chart = alt.Chart(df).mark_bar(size=20).encode(
    x=alt.X('Learned Status', axis=alt.Axis(labelAngle=0)),  # Set label angle to 0 for horizontal labels

    y=alt.Y('#'
    )
)


background = alt.Chart(df).mark_rect(
    cornerRadiusTopLeft=10,  # Rounded corners
    cornerRadiusTopRight=10,
    cornerRadiusBottomLeft=10,
    cornerRadiusBottomRight=10,
    fillOpacity=0.,  # Adjust fill opacity for visibility
).encode(
    x=alt.X('Learned Status', title='', axis=alt.Axis(labels=True)),  # Hide x-axis labels for background
    y=alt.Y('#', title='', axis=alt.Axis(labels=True)),  # Hide y-axis labels for background
    color=alt.value('Black')  # Set the background color
)

# Combine the background and bar chart
chart = background + chart
# Display the chart
st.altair_chart(chart, use_container_width=True)





#('''
df = pd.DataFrame(list)

# Set the title of the app
st.title("Word Definitions Table")
# Rename the columns if desired
df = df.iloc[:, 1:]

# Display the DataFrame as a table with new headers
st.table(df)

# ''')


#streamlit run test2.py