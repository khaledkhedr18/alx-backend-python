import sqlite3

# Connect to (or create) the users.db file
conn = sqlite3.connect('users.db')

# Create a cursor object to run SQL commands
cursor = conn.cursor()

# Create a table called users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')

# Insert some test users
cursor.executemany('''
INSERT INTO users (name, email) VALUES (?, ?)
''', [
    ("Alice", "alice@example.com"),
    ("Bob", "bob@example.com"),
    ("Charlie", "charlie@example.com")
])

# Commit the changes and close the connection
conn.commit()
conn.close()

print("users.db created and populated successfully.")
