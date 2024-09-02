import sqlite3

db_name = 'Bills.db'


def create_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the "person" table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS person (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        user_name TEXT NOT NULL
    )
    ''')

    # Create the "bill" table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bill (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        link_to_msg TEXT
    )
    ''')

    # Create the "CreditorDebtor" table (Assuming this is a junction table)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CreditorDebtor (
        person_id INTEGER,
        bill_id INTEGER,
        amount REAL,
        FOREIGN KEY (person_id) REFERENCES person(id),
        FOREIGN KEY (bill_id) REFERENCES bill(id),
        PRIMARY KEY (person_id, bill_id)
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def add_bill(parsed_data: dict, msg_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert the bill data into the bill table
    cursor.execute('''
    INSERT INTO bill (description, link_to_msg) 
    VALUES (?,?)
    ''', (parsed_data["description"], msg_id,))

    # Get the last inserted bill ID
    bill_id = cursor.lastrowid

    # Loop through each sequence and insert the person and CreditorDebtor data
    for sequence in parsed_data["sequences"]:
        # Check if the person already exists in the database
        cursor.execute('''
        SELECT id FROM person WHERE name = ?
        ''', (sequence["name"],))
        result = cursor.fetchone()
        person_id = result[0]

        # Convert the value to the correct sign
        value = int(sequence["value"])
        if sequence["sign"] == '-':
            value = -value

        # Insert the data into the CreditorDebtor table
        cursor.execute('''
        INSERT INTO CreditorDebtor (person_id, bill_id, amount)
        VALUES (?, ?, ?)
        ''', (person_id, bill_id, value))



    # Commit the transaction and close the connection
    conn.commit()
    conn.close()


def add_person(person_data: dict):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO person (name, user_name) 
            VALUES (?, ?)
        ''', (person_data['name'], person_data['user_name']))
        conn.commit()
        print(f"Person '{person_data['name']}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: Person with name '{person_data['name']}' already exists.")
    finally:
        conn.close()


def remove_person(person_data: dict):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM person WHERE name = ?', (person_data['name'],))
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Person removed successfully.")
        else:
            print("Person not found.")
            raise Exception
    finally:
        conn.close()
