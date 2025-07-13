import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Add the age column if it doesn't exist
cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER;")

# Optional: insert or update ages
cursor.execute("UPDATE users SET age = 30 WHERE id = 1")
cursor.execute("UPDATE users SET age = 22 WHERE id = 2")

conn.commit()
conn.close()
