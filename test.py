import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('testdb.db', check_same_thread=False)

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
        conn.commit()
    
    except sqlite3.Error:
        print("ERROR IN DELETING DB DATA")


def get_word_by_id(conn, word_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM vocabulary WHERE id = ?", (word_id,))
    result = cur.fetchone()  # fetchone() returns a single record or None
    return result



#add_data(conn, "thing", "thing_def", "unknown")
value = get_word_by_id(conn, 1)
print(value[1])