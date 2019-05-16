import os

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash

from DatabaseHandler import DatabaseHandler



app = Flask(__name__)


USERS_USERNAME_PW_INSERTION_QUERY = "INSERT INTO users (username, hash) VALUES(:username, :hash)"

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


DH = DatabaseHandler(db)



@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method != "POST":
        return render_template("register.html")

    if not request.form.get("username"):
        return ("must provide a username")
    elif not request.form.get("password"):
        return ("must provide a password", 400)

    password = request.form.get("password")
    # min 8 chars pw length, at least 1 upper char, at least 1 lower char, no spec chars, at least 1 digit

    if not request.form.get("confirmation"):
        return ("must confirm your password")
    elif request.form.get("password") != request.form.get("confirmation"):
        return ("password mismatch", 400)

    hashedPW = generate_password_hash(password)

    if not DH.isUsernameAvailable(request.form.get("username")):
        return "Username already taken"

    print("This should not be printed")


    DH.insertUsernameAndHashIntoUsers(request.form.get("username"), hashedPW)

    session["username"] = request.form.get("username")

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return "must provide username"

        elif not request.form.get("password"):
            return ("must provide password", 403)

        rows = DH.selectHashByUsernameFromUsers(request.form.get("username"))

        for data in rows:
            if not check_password_hash(data.hash, request.form.get("password")):
                print(request.form.get("password"))
                return "Ooops"

            session["id"] = data.id
            print(session["id"])

        #return redirect("/")
        return "Yeah, logged in!"

    else:
        return render_template("login.html")




