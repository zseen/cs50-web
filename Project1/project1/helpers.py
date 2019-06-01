from flask import redirect, session, render_template
from functools import wraps

#This method was originally provided for the 2018 CS50 course "Finance" exercise
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def getAverageOfNumsList(numsList):
    if numsList:
        return sum(numsList) / len(numsList)
    return 0


def renderApology(errorMessage, code=400):
    return render_template("apology.html", errorMessage=errorMessage), code