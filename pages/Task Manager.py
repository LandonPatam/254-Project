import sqlite3
import streamlit as st
import pandas as pd
import altair as alt
#from Home import completed_task_count

# Inline database setup
conn = sqlite3.connect('vocabulary2.db', check_same_thread=False)
cursor = conn.cursor()

completed_task_count = 0
tasks_to_be_completed = 0

# Create the tasks table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        completed TEXT NOT NULL DEFAULT 'incomplete'
    )
''')
conn.commit()


def add_task(conn, task):
    global tasks_to_be_completed
    try:
            cursor.execute("INSERT INTO tasks (task) VALUES (?)", (new_task,))
            conn.commit()
            st.success(f"Task '{new_task}' added successfully.")
            tasks_to_be_completed += 1
    except sqlite3.Error:
            st.error("Error: Task already exists or could not be added.")



st.title("Task Manager")

# FORM SECTION
with st.form(key="task_form"):
    new_task = st.text_input("Enter a new task")
    submit = st.form_submit_button(label="Add Task")
    if submit and new_task:
         add_task(conn, new_task)
         #st.write(f"Total Tasks {tasks_to_be_completed}")
        
# DISPLAYS TASK / DELETE TASK FUNCTIONALITY
st.header("Your Tasks")
cursor.execute("SELECT * FROM tasks")
tasks = cursor.fetchall()


if tasks:
    for task_id, task_name in tasks:
        st.write(task_name)
        if st.button(f"Complete {task_name}"):
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            #completed_task_count += 1
            st.rerun()
else:
    st.write("No tasks to display.")