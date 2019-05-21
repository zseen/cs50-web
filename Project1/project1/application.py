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
        return render_template("apology.html", errorMessage="Username not provided")

    if not password:
        return render_template("apology.html", errorMessage="Password not provided.")

    if not confirmation:
        return render_template("apology.html", errorMessage="Please confirm your password.")

    if password != confirmation:
        return render_template("apology.html", errorMessage="Password mismatch.")

    if databaseHandler.isUsernameTaken(username):
        return render_template("apology.html", errorMessage="Username already taken.")

    hashedPW = generate_password_hash(password)
    databaseHandler.registerUser(username, hashedPW)

    userData = databaseHandler.retrieveUserData(username)
    session["id"] = userData["id"]

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username:
        return render_template("apology.html", errorMessage="No username received.")

    if not password:
        return render_template("apology.html", errorMessage="No password provided.")

    userData = databaseHandler.retrieveUserData(username)
    if not userData:
        return render_template("apology.html", errorMessage="Incorrect username.")

    if not check_password_hash(userData["hashedpassword"], password):
        return render_template("apology.html", errorMessage="Incorrect password.")

    session["id"] = userData["id"]

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
        return render_template("apology.html", errorMessage="No isbn received.")

    book = databaseHandler.retrieveBookData(isbnReceived)
    if not book:
        return render_template("apology.html", errorMessage="Could not find book.")

    return render_template("book.html", book=book)
