import os

from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash
import requests

from loginDecorator import login_required
from DatabaseHandler import DatabaseHandler

GOODREADS_API_URL = "https://www.goodreads.com/book/review_counts.json"

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['JSON_SORT_KEYS'] = False
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

databaseHandler = DatabaseHandler(db)


@app.route("/")
def index():
    return render_template("layout.html", showMessage=True)


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if not username:
        return renderApology("Username not provided.")

    if not password:
        return renderApology("Password not provided.")

    if not confirmation:
        return renderApology("Please confirm your password.")

    if password != confirmation:
        return renderApology("Password mismatch.")

    if databaseHandler.isUsernameTaken(username):
        return renderApology("Username already taken.")

    hashedPW = generate_password_hash(password)
    databaseHandler.registerUser(username, hashedPW)

    userData = databaseHandler.retrieveUserData(username)
    session["id"] = userData["id"]

    return render_template("layout.html", username=username, showMessage=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username:
        return renderApology("No username received.")

    if not password:
        return renderApology("No password provided.")

    userData = databaseHandler.retrieveUserData(username)
    if not userData:
        return renderApology("Incorrect username.")

    if not check_password_hash(userData["hashed_password"], password):
        return renderApology("Incorrect password.")

    session["id"] = userData["id"]

    return render_template("layout.html", username=username, showMessage=True)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        return render_template("search.html")

    query = request.form.get("query")
    if not query:
        return renderApology("Please type in something to search for.")

    books = databaseHandler.retrieveBookDataByMultipleQueryTypes(query)
    if not books:
        return renderApology("Could not find book.")

    return render_template("bookSearchResults.html", books=books)


@app.route("/search/<isbn>", methods=["GET", "POST"])
@login_required
def showBookDetails(isbn):
    book = databaseHandler.retrieveBookDataByISBN(isbn)
    if not book:
        return renderApology("Could not find book")

    bookId = book["id"]
    userId = session["id"]

    reviewsFromOthers = databaseHandler.retrieveOthersReviewsOfBook(bookId, userId)
    allRatingsForBook = databaseHandler.retrieveAllRatingsForBook(bookId)
    reviewAndRatingFromCurrentUser = databaseHandler.retrieveCurrentUsersReviewAndRatingOfBook(bookId, userId)

    averageUsersRating = getAverageOfNumsList(allRatingsForBook)

    goodreadsRatingsCountAndAverageDict = getRatingsDataFromGoodreads(isbn)
    goodreadsRatingCount = goodreadsRatingsCountAndAverageDict["ratingCount"]
    goodreadsRatingAverage = goodreadsRatingsCountAndAverageDict["ratingAverage"]

    return render_template("reviewBook.html", book=book, reviewsFromOthers=reviewsFromOthers,
                           reviewFromCurrentUser=reviewAndRatingFromCurrentUser, averageUsersRating=averageUsersRating,
                           goodreadsRatingAverage=goodreadsRatingAverage, goodreadsRatingNum=goodreadsRatingCount)


@app.route("/addBookReview/<isbn>", methods=["GET", "POST"])
@login_required
def addBookReview(isbn):
    book = databaseHandler.retrieveBookDataByISBN(isbn)
    if not book:
        return render_template("apology.html", errorMessage="No book found.")

    bookId = book["id"]

    userId = session["id"]
    review = request.form.get("review")
    rating = request.form.get("rating")

    if not review or not rating:
        return renderApology("You haven't added a review or rating.")

    canUserAddReview = databaseHandler.canUserAddReviewAndRatingForBook(bookId, userId)
    if not canUserAddReview:
        return renderApology("Sorry, you have already reviewed this book.")

    databaseHandler.addBookReviewAndRating(rating, review, bookId, userId)

    reviewsFromOthers = databaseHandler.retrieveOthersReviewsOfBook(bookId, userId)
    allRatingsForBook = databaseHandler.retrieveAllRatingsForBook(bookId)

    averageUsersRating = getAverageOfNumsList(allRatingsForBook)

    goodreadsRatingsCountAndAverageDict = getRatingsDataFromGoodreads(isbn)
    goodreadsRatingCount = goodreadsRatingsCountAndAverageDict["ratingCount"]
    goodreadsRatingAverage = goodreadsRatingsCountAndAverageDict["ratingAverage"]

    return render_template("book.html", book=book, reviewsFromOthers=reviewsFromOthers, currentUserReview=review,
                           currentUserRating=rating, averageUsersRating=averageUsersRating,
                           goodreadsRatingAverage=goodreadsRatingAverage, goodreadsRatingNum=goodreadsRatingCount)


@app.route("/api/<isbn>", methods=["GET"])
def getAPIaccess(isbn):
    book = databaseHandler.retrieveBookDataByISBN(isbn)
    if not book:
        return renderApology("Invalid ISBN. Please try again.", code=404)

    bookId = book["id"]
    ratings = databaseHandler.retrieveAllRatingsForBook(bookId)
    ratingsCount = len(ratings)
    averageRating = getAverageOfNumsList(ratings)

    return jsonify(
        title=book["title"],
        author=book["author"],
        year=int(book["year"]),
        isbn=book["isbn"],
        review_count=ratingsCount,
        average_score=averageRating)


def getRatingsDataFromGoodreads(isbn):
    dataRequest = requests.get(GOODREADS_API_URL,
                               params={"key": "", "isbns": isbn})

    requestedData = (dataRequest.json())
    if not requestedData:
        renderApology("Cannot find book")

    if len(requestedData["books"]) > 1:
        renderApology("Unexpected error: multiple books exist with same isbn")

    bookDetails = requestedData["books"]
    ratingCount = bookDetails[0]["work_ratings_count"]
    ratingAverage = bookDetails[0]["average_rating"]

    data = {"ratingCount": ratingCount, "ratingAverage": ratingAverage}
    return data


def getAverageOfNumsList(numsList):
    if len(numsList) == 0:
        return 0

    return sum(numsList) / len(numsList)


def renderApology(errorMessage, code=400):
    return render_template("apology.html", errorMessage=errorMessage), code
