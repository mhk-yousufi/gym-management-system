import sqlite3

def get_connection():
    """Creates a database connection with column-name access enabled."""
    connection = sqlite3.connect('database/gym.db')
    connection.row_factory = sqlite3.Row
    return connection

def add_member(name, phone, join_date, plan_id):
    """Adds a new member and returns their new id."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO members (name, phone, join_date, plan_id)
        VALUES (?, ?, ?, ?)
    """, (name, phone, join_date, plan_id))
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return new_id

def get_all_members():
    """Returns a list of all members."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    connection.close()
    return members

def get_all_plans():
    """Returns a list of all membership plans."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM membership_plans")
    plans = cursor.fetchall()
    connection.close()
    return plans

def update_member(member_id, name, phone, join_date, plan_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE members
        SET name = ?, phone = ?, join_date = ?, plan_id = ?
        WHERE id = ?
    """, (name, phone, join_date, plan_id, member_id))
    conn.commit()
    conn.close()

def delete_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()

def get_member_by_id(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    member = cursor.fetchone()
    conn.close()
    return member