from flask import Flask, render_template, request, redirect, session
from db_helpers import get_all_members, add_member, get_all_plans, get_member_by_id, update_member, delete_member, add_payment, get_payments_for_member, get_member_status, get_dashboard_stats, verify_login, get_member_by_user_id
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        if session.get('role') != 'admin':
            return "Access denied. Admins only.", 403
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)

app.secret_key = 'gym-management-secret-key-change-this-later'

@app.route('/')
def home():
    return "Gym Management System is running!"

@app.route('/members')
@admin_required
def members_list():
    members = get_all_members()
    return render_template('members.html', members=members, get_status=get_member_status)

@app.route('/members/add', methods=['GET', 'POST'])
@admin_required
def add_member_route():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        join_date = request.form['join_date']
        plan_id = request.form['plan_id']
        add_member(name, phone, join_date, plan_id)
        return redirect('/members')
    plans = get_all_plans()
    return render_template('add_member.html', plans=plans)

@app.route('/members/edit/<int:member_id>', methods=['GET', 'POST'])
@admin_required
def edit_member_route(member_id):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        join_date = request.form['join_date']
        plan_id = request.form['plan_id']
        update_member(member_id, name, phone, join_date, plan_id)
        return redirect('/members')
    member = get_member_by_id(member_id)
    plans = get_all_plans()
    return render_template('edit_member.html', member=member, plans=plans)

@app.route('/members/delete/<int:member_id>')
@admin_required
def delete_member_route(member_id):
    delete_member(member_id)
    return redirect('/members')

@app.route('/members/<int:member_id>/pay', methods=['GET', 'POST'])
@admin_required
def record_payment_route(member_id):
    if request.method == 'POST':
        plan_id = request.form['plan_id']
        amount = request.form['amount']
        payment_date = request.form['payment_date']

        add_payment(member_id, plan_id, amount, payment_date)
        return redirect('/members')

    member = get_member_by_id(member_id)
    plans = get_all_plans()
    payments = get_payments_for_member(member_id)
    return render_template('add_payment.html', member=member, plans=plans, payments=payments)

@app.route('/dashboard')
@admin_required
def dashboard():
    stats = get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = verify_login(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            if user['role'] == 'admin':
                return redirect('/dashboard')
            else:
                return redirect('/my-profile')
        else:
            return render_template('login.html', error="Wrong username or password")

    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/my-profile')
@login_required
def my_profile():
    member = get_member_by_user_id(session['user_id'])
    if member is None:
        return "No member profile linked to this account."

    status = get_member_status(member['id'])
    payments = get_payments_for_member(member['id'])
    return render_template('my_profile.html', member=member, status=status, payments=payments)

if __name__ == '__main__':
    app.run(debug=True)