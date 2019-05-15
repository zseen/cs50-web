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
    """Register user"""
    session.clear()
    if request.method != "POST":
        return render_template("register.html")

    if not request.form.get("username"):
        return ("must provide a username", 400)
    elif not request.form.get("password"):
        return ("must provide a password", 400)

    password = request.form.get("password")
    # min 8 chars pw length, at least 1 upper char, at least 1 lower char, no spec chars, at least 1 digit

    if not request.form.get("confirmation"):
        return ("must confirm your password", 400)
    elif request.form.get("password") != request.form.get("confirmation"):
        return ("password mismatch", 400)


    hashedPW = generate_password_hash(password)

    newUser = DH.insertUsernameAndHashIntoUsers(request.form.get("username"), hashedPW)

    if not newUser:
        return "Username already taken"

    for iter in session:
        session["user_id"] = iter[0]

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return "must provide username"

        # Ensure password was submitted
        elif not request.form.get("password"):
            return ("must provide password", 403)

        # Query database for username
        rows = DH.selectHashByUsernameFromUsers(request.form.get("username"))

        for data in rows:
            if not check_password_hash(data.hash, request.form.get("password")):
                print(request.form.get("password"))
                return "Ooops"
            session["user_id"] = ###??????
            print(session["user_id"])

        # Redirect user to home page
        #return redirect("/")
        return "Yeah, logged in!"

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")




