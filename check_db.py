import sqlite3

connection = sqlite3.connect('database/gym.db')
cursor = connection.cursor()

# Ask SQLite for a list of all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")

connection.close()
