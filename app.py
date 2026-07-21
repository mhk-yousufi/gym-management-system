from flask import Flask, render_template
from db_helpers import get_all_members

app = Flask(__name__)

@app.route('/')
def home():
    return "Gym Management System is running!"

@app.route('/members')
def members_list():
    members = get_all_members()
    return render_template('members.html', members=members)

if __name__ == '__main__':
    app.run(debug=True)