from flask import Flask
from database.__init__ import conn
from views.user_view import user
from views.task_view import task
#pip install flask

app = Flask(__name__)

print(conn.database)

app.register_blueprint(user)
app.register_blueprint(task)

@app.route("/")
def index():
    projectInfo = {"Project Name": "Task Tracker Project", "Team members": ["Viraj Patel", "Aryan Handa", "Payal Rangra", "Manpreet Kaur","Dil Raval"]}
    return projectInfo

if __name__ == "__main__":
    app.run()

#flask --app app run