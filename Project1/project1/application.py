import os

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash
from loginDecorator import login_required

from DatabaseHandler import DatabaseHandler


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

databaseHandler = DatabaseHandler(db)


@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "GET":
        return render_template("register.html")

    if not request.form.get("username"):
        return "must provide a username"
    elif not request.form.get("password"):
        return "must provide a password"

    password = request.form.get("password")
    username = request.form.get("username")

    if not request.form.get("confirmation"):
        return "must confirm your password"
    elif password != request.form.get("confirmation"):
        return "password mismatch"

    if databaseHandler.isUsernameTaken(username):
        return "Username already taken"

    hashedPW = generate_password_hash(password)
    databaseHandler.registerUser(username, hashedPW)

    userData = databaseHandler.retrieveUserData(username)
    for data in userData:
        session["id"] = data.id

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    if not request.form.get("username"):
        return "must provide username"

    elif not request.form.get("password"):
        return "must provide password"

    username = request.form.get("username")
    password = request.form.get("password")

    rows = databaseHandler.retrieveUserData(username)
    for data in rows:
        if not check_password_hash(data.hash, password):
            return "Incorrect password."

        session["id"] = data.id

    return redirect("/")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        return render_template("search.html")

    isbnReceived = request.form.get("isbn")
    if not isbnReceived:
        return "No isbn received"

    book = databaseHandler.retrieveBookData(isbnReceived)
    if not book:
        return "Could not find book"
    print(book)  #  Temporary solution, will return a book html page later
    return redirect("/")
