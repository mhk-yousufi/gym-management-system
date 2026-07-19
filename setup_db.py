import sqlite3

# Connect to (or create) the database file
connection = sqlite3.connect('database/gym.db')

# Read our schema file
with open('database/schema.sql', 'r') as f:
    schema = f.read()

# Run all the CREATE TABLE statements
connection.executescript(schema)

# Save changes and close
connection.commit()
connection.close()

print("Database created successfully!")