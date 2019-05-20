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

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if not username:
        return "must provide a username"
    elif not password:
        return "must provide a password"

    if not confirmation:
        return "must confirm your password"
    elif password != confirmation:
        return "password mismatch"

    if databaseHandler.isUsernameTaken(username):
        return "Username already taken"

    hashedPW = generate_password_hash(password)
    databaseHandler.registerUser(username, hashedPW)

    userData = databaseHandler.retrieveUserData(username)
    session["id"] = userData[0]["id"]

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "GET":
        return render_template("login.html")

    if not username:
        return "must provide username"

    elif not password:
        return "must provide password"

    userData = databaseHandler.retrieveUserData(username)
    print(userData)
    #print(len(userData))
    if not check_password_hash(userData[0]["hash"], password):
        return "Incorrect password."

    session["id"] = userData[0]["id"]

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
    print(book)  # Temporary solution, will return a book html page later
    return redirect("/")
