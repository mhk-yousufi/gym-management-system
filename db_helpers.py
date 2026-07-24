import sqlite3

from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

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

def get_member_status(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT payments.payment_date, membership_plans.duration_months
        FROM payments
        JOIN membership_plans ON payments.plan_id = membership_plans.id
        WHERE payments.member_id = ?
        ORDER BY payments.payment_date DESC
        LIMIT 1
    """, (member_id,))
    last_payment = cursor.fetchone()
    conn.close()

    if last_payment is None:
        return "No payments yet"

    payment_date = datetime.strptime(last_payment['payment_date'], '%Y-%m-%d')
    duration_months = last_payment['duration_months']
    expiry_date = payment_date + timedelta(days=duration_months * 30)

    if expiry_date < datetime.now():
        return f"Expired on {expiry_date.strftime('%Y-%m-%d')}"
    else:
        return f"Active until {expiry_date.strftime('%Y-%m-%d')}"

def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()

    # total members
    cursor.execute("SELECT COUNT(*) as total FROM members")
    total_members = cursor.fetchone()['total']

    # revenue this month
    current_month = datetime.now().strftime('%Y-%m')
    cursor.execute("""
        SELECT SUM(amount) as total_revenue
        FROM payments
        WHERE payment_date LIKE ?
    """, (current_month + '%',))
    result = cursor.fetchone()
    monthly_revenue = result['total_revenue'] if result['total_revenue'] else 0

    conn.close()

    # active vs expired - reuse the status function we already wrote
    all_members = get_all_members()
    active_count = 0
    expired_count = 0
    no_payment_count = 0

    for m in all_members:
        status = get_member_status(m['id'])
        if status.startswith("Active"):
            active_count += 1
        elif status.startswith("Expired"):
            expired_count += 1
        else:
            no_payment_count += 1

    return {
        'total_members': total_members,
        'monthly_revenue': monthly_revenue,
        'active_count': active_count,
        'expired_count': expired_count,
        'no_payment_count': no_payment_count
    }

def create_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    hashed = generate_password_hash(password)
    cursor.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    """, (username, hashed, role))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_login(username, password):
    user = get_user_by_username(username)
    if user is None:
        return None
    if check_password_hash(user['password_hash'], password):
        return user
    return None

def create_member_login(member_id, username, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed = generate_password_hash(password)
    cursor.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    """, (username, hashed, "member"))

    new_user_id = cursor.lastrowid

    cursor.execute("""
        UPDATE members SET user_id = ? WHERE id = ?
    """, (new_user_id, member_id))

    conn.commit()
    conn.close()

def get_member_by_user_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE user_id = ?", (user_id,))
    member = cursor.fetchone()
    conn.close()
    return member