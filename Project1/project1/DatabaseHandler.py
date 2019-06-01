from unittest.mock import Mock
from unittest import TestCase
import unittest
import re


class DatabaseHandler:
    def __init__(self, database):
        self._database = database

    def registerUser(self, username, hashedPassword):
        self._database.execute("INSERT INTO users (username, hashed_password) VALUES(:username, :hashed_password)",
                               {"username": username,
                                "hashed_password": hashedPassword})
        self._database.commit()

    def retrieveUserData(self, username):
        userDataRows = self._database.execute("SELECT hashed_password, id FROM users WHERE username = :username",
                                              {"username": username}).fetchall()

        if not userDataRows:
            return None

        numRows = sum(1 for _ in userDataRows)
        if numRows > 1:
            return "Unexpected error: multiple users exist with username"

        return userDataRows[0]

    def isUsernameTaken(self, username):
        preExistingUsername = self._database.execute("SELECT username FROM users WHERE username = :username",
                                                     {"username": username}).fetchone()

        return (preExistingUsername is not None)

    def retrieveBookDataByISBN(self, isbn):
        book = self._database.execute("SELECT title, author, year, isbn, id FROM books WHERE isbn = :isbn",
                                                     {"isbn": isbn}).fetchone()
        if not book:
            return None

        return book

    def retrieveBookDataByMultipleQueryTypes(self, query):
        query = query.strip()

        # isbn consists of 10 chars: 9 ints and ends with either an int or with 'X', regex also considers an ending with 'x'
        isQueryIsbn = re.search(r'^[0-9]{9}[X]|[x]|[0-9]]', query)
        if isQueryIsbn and query[-1] == "x":
            query = query[:9] + "X" # capitalizes the ending 'x' so that SQL query can find the book by isbn
        else:
            query = query.capitalize()

        modifiedQuery = "%" + query + "%"
        books = self._database.execute(
            "SELECT title, author, year, isbn, id FROM books WHERE isbn LIKE :modifiedQuery OR title LIKE :modifiedQuery OR author LIKE :modifiedQuery",
            {'modifiedQuery': modifiedQuery}).fetchall()

        if not books:
            return None

        booksList = []
        for book in books:
            booksList.append(book)

        return booksList

    def isBookReviewAlreadyAdded(self, userId, bookId):
        preExistingReview = self._database.execute(
            "SELECT review FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
            {"user_id": userId, "book_id": bookId}).fetchone()

        return (preExistingReview is not None)

    def isBookRatingAlreadyAdded(self, userId, bookId):
        preExistingRating = self._database.execute(
            "SELECT rating FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
            {"user_id": userId, "book_id": bookId}).fetchone()

        return (preExistingRating is not None)

    def addBookReviewAndRating(self, rating, review, user_id, book_id):
        self._database.execute(
            "INSERT INTO reviews (user_id, book_id, rating, review) VALUES (:user_id, :book_id, :rating, :review)",
            {"user_id": user_id, "book_id": book_id, "rating": rating, "review": review})
        self._database.commit()

    def retrieveOthersReviewsOfBook(self, bookId, userId):
        allReviews = self._database.execute(
            "SELECT review FROM reviews WHERE book_id = :book_id AND NOT user_id = :user_id",
            {"book_id": bookId, "user_id": userId}).fetchall()

        return allReviews

    def retrieveOthersRatingsOfBook(self, bookId, userId):
        othersRatings = self._database.execute(
            "SELECT rating FROM reviews WHERE book_id = :book_id AND NOT user_id = :user_id",
            {"book_id": bookId, "user_id": userId}).fetchall()

        othersRatingsList = []
        for rating in othersRatings:
            othersRatingsList.append(rating)

        return othersRatingsList

    def retrieveCurrentUsersReviewAndRatingOfBook(self, bookId, userId):
        currentUsersReviewAndRating = self._database.execute(
            "SELECT rating, review FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
            {"user_id": userId, "book_id": bookId}).fetchone()

        return currentUsersReviewAndRating

    def retrieveAllRatingsForBook(self, bookId):
        ratings = self._database.execute("SELECT rating FROM reviews WHERE book_id = :book_id",
                                         {"book_id": bookId}).fetchall()

        if not ratings:
            return None

        allRatingsList = []
        for rating in ratings:
            allRatingsList.append(rating)

        return allRatingsList


class MockTestDatabaseHandler(TestCase):
    def setUp(self):
        self.mockDB = Mock()
        self.databaseHandler = DatabaseHandler(self.mockDB)

    def test_registerUser_correctSqlIsExecuted(self):
        self.databaseHandler.registerUser("Bookworm45", "adf43ef91ba")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with(
            "INSERT INTO users (username, hashed_password) VALUES(:username, :hashed_password)",
            {'username': 'Bookworm45', 'hashed_password': 'adf43ef91ba'})
        self.mockDB.commit.assert_called_once()

    def test_retrieveUserData_correctUserDataReturned(self):
        self.mockFetchAllResult = Mock()
        self.mockFetchAllResult.fetchall.return_value = [{"hashed_password": "adf43ef91ba", "id": 4}]
        self.mockDB.execute.return_value = self.mockFetchAllResult

        userData = self.databaseHandler.retrieveUserData("Bookworm45")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT hashed_password, id FROM users WHERE username = :username",
                                               {'username': 'Bookworm45'})

        self.assertEquals(4, userData["id"])
        self.assertEquals("adf43ef91ba", userData["hashed_password"])

    def test_retrieveUserData_notExistingUserReturnNone(self):
        self.mockFetchAllResult = Mock()
        self.mockFetchAllResult.fetchall.return_value = None
        self.mockDB.execute.return_value = self.mockFetchAllResult

        userData = self.databaseHandler.retrieveUserData("Bookworm45")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT hashed_password, id FROM users WHERE username = :username",
                                               {'username': 'Bookworm45'})

        self.assertEquals(None, userData)

    def test_isUsernameTaken_calledWithExistingUser_returnTrue(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = [{"username": "Bookworm45"}]
        self.mockDB.execute.return_value = self.mockFetchResult

        isTaken = self.databaseHandler.isUsernameTaken("Bookworm45")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT username FROM users WHERE username = :username",
                                               {'username': 'Bookworm45'})

        self.assertTrue(isTaken)

    def test_retrieveBookData_calledWithPartialISBN_allDataReturned(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchall.return_value = [{"title": "ThisGoodBook", "author": "Amazing Author",
                                                       "year": "2012", "isbn": "1234567", "id": "2"}]
        self.mockDB.execute.return_value = self.mockFetchResult

        bookData = self.databaseHandler.retrieveBookDataByMultipleQueryTypes("123456")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with(
            "SELECT title, author, year, isbn, id FROM books WHERE isbn LIKE :modifiedQuery OR title LIKE :modifiedQuery OR author LIKE :modifiedQuery",
            {'modifiedQuery': '%123456%'})

        self.assertEquals("ThisGoodBook", bookData[0]["title"])
        self.assertEquals("Amazing Author", bookData[0]["author"])
        self.assertEquals("2012", bookData[0]["year"])
        self.assertEquals("1234567", bookData[0]["isbn"])
        self.assertEquals("2", bookData[0]["id"])

    def test_isBookRatingAlreadyAdded_calledWithExistingRating_returnTrue(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = [{"rating": "4.6"}]
        self.mockDB.execute.return_value = self.mockFetchResult

        isTaken = self.databaseHandler.isBookRatingAlreadyAdded("4", "3")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with(
            "SELECT rating FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
            {"user_id": "4", "book_id": "3"})

        self.assertTrue(isTaken)

    def test_addBookReview_correctSqlIsExecuted(self):
        self.databaseHandler.addBookReviewAndRating("5.0", "goodBook", "1", "2")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with(
            "INSERT INTO reviews (user_id, book_id, rating, review) VALUES (:user_id, :book_id, :rating, :review)",
            {"user_id": "1", "book_id": "2", "rating": "5.0", "review": "goodBook"})

        self.mockDB.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
