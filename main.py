from flask import Flask, request, Response
import json
from settings import *

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return "Заглушка для приложения JoteroApp"


@app.route("/add_quiz", methods=["GET"])
def add_quiz():
    quiz = request.args("quiz")

    with open(quiz_list_file_name) as quiz_list_json:
        json.dump(quiz, quiz_list_json)


@app.route("/get_quiz_list", methods=["GET"])
def send_quiz_list():
    login = request.args["login"]
    password = request.args["password"]

    with open(users_file_name) as user_json:
        users = json.load(user_json)

    if login not in users:
        return {"error": "Login does not exist"}

    if password != users[login][password]:
        return {"error": "Invalid password"}

    return {"available_quiz": [],
            "completed_quiz": []}


@app.route("/register", methods=["GET"])
def register():
    login = request.args["login"]
    password = request.args["password"]
    name = request.args["name"]
    surname = request.args["surname"]
    middleName = request.args["middleName"]
    age = request.args["age"]
    city = request.args["city"]
    sex = request.args["sex"]

    with open(users_file_name, "r") as users_json:
        users = json.load(users_json)["users"]

    if login in users:
        return {"error": "Login is already taken"}

    new_user = {
        "password": password,
        "name": name,
        "surname": surname,
        "middleName": middleName,
        "age": age,
        "city": city,
        "sex": sex,
        "available_quiz": [],
        "completed_quiz": []
    }

    users[login] = new_user

    with open(users_file_name, "w") as users_json:
        json.dump(users, users_json)

    return {
        "register_result": True
    }


@app.route("/login", methods=["GET"])
def login():
    login = request.args["login"]
    password = request.args["password"]

    with open(users_file_name) as user_json:
        users = json.load(user_json)["users"]

    if login not in users:
        return {"error": "Login does not exist"}

    if password != users[login]["password"]:
        return {"error": "Invalid password"}

    return {"login_result": True}


@app.route("/check_login", methods=["GET"])
def check_login():
    login = request.args["login"]

    with open(users_file_name) as user_json:
        users = json.load(user_json)["users"]

    if login in users:
        return {"result": False}

    return {"result": True}


@app.route("/test", methods=["GET", "POST"])
def test():
    a = request.args["a"]
    b = request.args["b"]

    return f"a = {a}, b = {b}"


app.run()
