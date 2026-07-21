from flask import Flask, render_template, request, redirect
from db_helpers import get_all_members, add_member, get_all_plans

app = Flask(__name__)

@app.route('/')
def home():
    return "Gym Management System is running!"

@app.route('/members')
def members_list():
    members = get_all_members()
    return render_template('members.html', members=members)

@app.route('/members/add', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True)