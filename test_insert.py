import sqlite3

connection = sqlite3.connect('database/gym.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# --- INSERT a membership plan ---
cursor.execute("""
    INSERT INTO membership_plans (plan_name, price, duration_months)
    VALUES (?, ?, ?)
""", ("Monthly", 3000, 1))

# --- INSERT a member, linked to that plan ---
cursor.execute("""
    INSERT INTO members (name, phone, join_date, plan_id)
    VALUES (?, ?, ?, ?)
""", ("Ahmed Khan", "0300-1234567", "2026-07-19", 1))

connection.commit()

# --- READ it back ---
cursor.execute("SELECT * FROM members")
rows = cursor.fetchall()

print("Members in database:")
for row in rows:
    print(f"ID: {row['id']}, Name: {row['name']}, Phone: {row['phone']}, Plan ID: {row['plan_id']}")

connection.close()