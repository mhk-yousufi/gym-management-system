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

def add_payment(member_id, plan_id, amount, payment_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO payments (member_id, plan_id, amount, payment_date)
        VALUES (?, ?, ?, ?)
    """, (member_id, plan_id, amount, payment_date))
    conn.commit()
    conn.close()

def get_payments_for_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT payments.*, membership_plans.plan_name
        FROM payments
        JOIN membership_plans ON payments.plan_id = membership_plans.id
        WHERE payments.member_id = ?
        ORDER BY payment_date DESC
    """, (member_id,))
    payments = cursor.fetchall()
    conn.close()
    return payments