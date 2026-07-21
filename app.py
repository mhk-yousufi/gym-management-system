from flask import Flask
from db_helpers import get_all_members

app = Flask(__name__)

@app.route('/')
def home():
    return "Gym Management System is running!"

@app.route('/members')
def members_list():
    members = get_all_members()
    output = "<h1>All Members</h1><ul>"
    for m in members:
        output += f"<li>{m['name']} — {m['phone']}</li>"
    output += "</ul>"
    return output

if __name__ == '__main__':
    app.run(debug=True)