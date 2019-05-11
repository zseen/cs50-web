import os

from flask import Flask, session
from flask_session import Session
from flask import Flask, flash, redirect, render_template, request, session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import re

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


@app.route("/")
def index():
    return render_template("register.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method != "POST":
        return render_template("register.html")

    if not request.form.get("username"):
        return apology("must provide a username", 400)
    elif not request.form.get("password"):
        return apology("must provide a password", 400)

    password = request.form.get("password")
    # min 8 chars pw length, at least 1 upper char, at least 1 lower char, no spec chars, at least 1 digit
    # if not checkPasswordValid(password, MIN_PW_LENGTH):
        # return apology("Your password does not meet the requirements", 400)
    # elif not request.form.get("confirmation"):
        # return apology("must confirm your password", 400)
    # elif request.form.get("password") != request.form.get("confirmation"):
        # return apology("password mismatch", 400)

    hashedPW = generate_password_hash(request.form.get("password"))
    newRegisteredUser = db.execute(USERS_USERNAME_PW_INSERTION_QUERY,
                                    username=request.form.get("username"),
                                    hash=hashedPW)
    if not newRegisteredUser:
        return apology("username already taken", 400)

    session["user_id"] = newRegisteredUser
    return redirect("/")

