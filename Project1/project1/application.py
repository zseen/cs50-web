import os

from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash
import requests

from loginDecorator import login_required

from DatabaseHandler import DatabaseHandler

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

    if not check_password_hash(userData["hashed_password"], password):
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

    query = request.form.get("query")
    if not query:
        return render_template("apology.html", errorMessage="Please type in something to search for.")

    books = databaseHandler.retrieveBookData(query)
    print(books)

    if not books:
        return render_template("apology.html", errorMessage="Could not find book.")

    return render_template("bookSearchResults.html", books=books)


@app.route("/search/<isbn>", methods=["GET", "POST"])
@login_required
def showBookDetails(isbn):
    book = databaseHandler.retrieveBookData(isbn)
    bookId = book[0]["id"]
    userId = session["id"]

    reviewsFromOthers = databaseHandler.retrieveOthersReviewsOfBook(bookId, userId)
    ratingsFromOthers = databaseHandler.retrieveOthersRatingsOfBook(bookId, userId)
    reviewAndRatingFromCurrentUser = databaseHandler.retrieveCurrentUsersReviewAndRatingOfBook(bookId, userId)

    averageUsersRating = 0
    if ratingsFromOthers:
        averageUsersRating = sum(ratingsFromOthers) / len(ratingsFromOthers)

    ratingsCountAndAverageGoodReadsDict = getGoodReadsRating(isbn)
    ratingCountGR = ratingsCountAndAverageGoodReadsDict["ratingCount"]
    ratingAverageGR = ratingsCountAndAverageGoodReadsDict["ratingAverage"]

    # "book" is list, so the book information is in the [0]th element of the list
    return render_template("reviewBook.html", book=book[0], reviewsFromOthers=reviewsFromOthers,
                           reviewOfCurrentUser=reviewAndRatingFromCurrentUser, averageUsersRating=averageUsersRating,
                           goodReadsRatingAverage=ratingAverageGR, goodReadsRatingNum=ratingCountGR)


@app.route("/addBookReview/<isbn>", methods=["GET", "POST"])
@login_required
def addBookReview(isbn):
    book = databaseHandler.retrieveBookData(isbn)

    userId = session["id"]
    bookId = book[0]["id"]
    review = request.form.get("review")
    rating = request.form.get("rating")

    if databaseHandler.isBookReviewAlreadyAdded(userId, bookId):
        return render_template("apology.html", errorMessage="You have already submitted a review.")

    if databaseHandler.isBookRatingAlreadyAdded(userId, bookId):
        return render_template("apology.html", errorMessage="You have already submitted a rating.")

    databaseHandler.addBookReviewAndRating(rating, review, userId, bookId)

    reviewsFromOthers = databaseHandler.retrieveOthersReviewsOfBook(bookId, userId)
    ratingsFromOthers = databaseHandler.retrieveOthersRatingsOfBook(bookId, userId)

    averageUsersRating = 0
    # current user's rating is not calculated in the average
    if ratingsFromOthers:
        averageUsersRating = sum(ratingsFromOthers) / len(ratingsFromOthers)

    ratingsCountAndAverageGoodReadsDict = getGoodReadsRating(isbn)
    ratingCountGR = ratingsCountAndAverageGoodReadsDict["ratingCount"]
    ratingAverageGR = ratingsCountAndAverageGoodReadsDict["ratingAverage"]

    return render_template("book.html", book=book[0], reviewsFromOthers=reviewsFromOthers, currentUserReview=review,
                           currentUserRating=rating, averageUsersRating=averageUsersRating,
                           goodReadsRatingAverage=ratingAverageGR, goodReadsRatingNum=ratingCountGR)


def getGoodReadsRating(isbn):
    dataRequest = requests.get("https://www.goodreads.com/book/review_counts.json",
                               params={"key": "", "isbns": isbn})

    requestedData = (dataRequest.json())
    bookDetails = requestedData["books"]
    ratingCount = bookDetails[0]["work_ratings_count"]
    ratingAverage = bookDetails[0]["average_rating"]

    data = {"ratingCount": ratingCount, "ratingAverage": ratingAverage}
    return data


@app.route("/api/<isbn>", methods=["GET"])
def getAPIaccess(isbn):
    book = databaseHandler.retrieveBookData(isbn)
    if not book:
        return render_template("apology.html", errorMessage="Invalid ISBN. "
                                                            "Please try again.")
    book = book[0]
    bookId = book["id"]
    ratings = databaseHandler.retrieveAllRatingsForBook(bookId)
    ratingsCount = 0
    averageRating = 0

    if ratings:
        ratingsCount = len(ratings)
        averageRating = sum(ratings) / len(ratings)

    return jsonify(
        title=book["title"],
        author=book["author"],
        year=int(book["year"]),
        isbn=book["isbn"],
        review_count=ratingsCount,
        average_score=averageRating
    )
