from unittest.mock import Mock
from unittest import TestCase
import unittest
from databaseHandlerHelper import extractSingleColumnValues


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

        return book

    def retrieveBookDataByMultipleQueryTypes(self, query):
        query = query.strip().lower()

        queryLikeClause = "%" + query + "%"
        bookRows = self._database.execute(
            "SELECT title, author, year, isbn, id FROM books WHERE LOWER (isbn) LIKE :queryLikeClause OR LOWER (title) LIKE :queryLikeClause OR LOWER (author) LIKE :queryLikeClause",
            {'queryLikeClause': queryLikeClause}).fetchall()

        if not bookRows:
            return []

        return bookRows

    def canUserAddReviewAndRatingForBook(self, userId, bookId):
        preExistingReviewAndRating = self._database.execute(
            "SELECT rating, review FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
            {"user_id": userId, "book_id": bookId}).fetchone()

        return (preExistingReviewAndRating is None)

    def addBookReviewAndRating(self, rating, review, user_id, book_id):
        self._database.execute(
            "INSERT INTO reviews (user_id, book_id, rating, review) VALUES (:user_id, :book_id, :rating, :review)",
            {"user_id": user_id, "book_id": book_id, "rating": rating, "review": review})
        self._database.commit()

    def retrieveOthersReviewsOfBook(self, bookId, userId):
        rows = self._database.execute(
            "SELECT review FROM reviews WHERE book_id = :book_id AND NOT user_id = :user_id",
            {"book_id": bookId, "user_id": userId}).fetchall()

        reviews = extractSingleColumnValues(rows, "review")
        return reviews

    def retrieveOthersRatingsOfBook(self, bookId, userId):
        rows = self._database.execute(
            "SELECT rating FROM reviews WHERE book_id = :book_id AND NOT user_id = :user_id",
            {"book_id": bookId, "user_id": userId}).fetchall()

        ratings = extractSingleColumnValues(rows, "rating")
        return ratings

    def retrieveCurrentUsersReviewAndRatingOfBook(self, bookId, userId):
        currentUsersReviewAndRating = self._database.execute(
            "SELECT rating, review FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
            {"user_id": userId, "book_id": bookId}).fetchone()

        return currentUsersReviewAndRating

    def retrieveAllRatingsForBook(self, bookId):
        rows = self._database.execute("SELECT rating FROM reviews WHERE book_id = :book_id",
                                      {"book_id": bookId}).fetchall()

        ratings = extractSingleColumnValues(rows, "rating")
        return ratings


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
        self.mockFetchAllResult.fetchall.return_value = [{"hashed_password": "adf43ef91ba", "id": 1234}]
        self.mockDB.execute.return_value = self.mockFetchAllResult

        userData = self.databaseHandler.retrieveUserData("Bookworm45")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT hashed_password, id FROM users WHERE username = :username",
                                               {'username': 'Bookworm45'})

        self.assertEquals(1234, userData["id"])
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

    def test_retrieveBookData_calledWithPartialFirstName_allDataReturned(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchall.return_value = [{"title": "ThisGoodBook", "author": "Amazing Author",
                                                       "year": "2012", "isbn": "1234567", "id": "9998"},
                                                      {"title": "ThatNiceStory", "author": "Amazing Author",
                                                       "year": "1991", "isbn": "7654321", "id": "9999"}]
        self.mockDB.execute.return_value = self.mockFetchResult

        booksData = self.databaseHandler.retrieveBookDataByMultipleQueryTypes("Amazin")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with(
            "SELECT title, author, year, isbn, id FROM books WHERE LOWER (isbn) LIKE :queryLikeClause OR LOWER (title) LIKE :queryLikeClause OR LOWER (author) LIKE :queryLikeClause",
            {'queryLikeClause': "%amazin%"})

        firstBook = booksData[0]
        secondBook = booksData[1]

        self.assertEquals("ThisGoodBook", firstBook["title"])
        self.assertEquals("Amazing Author", firstBook["author"])
        self.assertEquals("2012", firstBook["year"])
        self.assertEquals("1234567", firstBook["isbn"])
        self.assertEquals("9998", firstBook["id"])

        self.assertEquals("ThatNiceStory", secondBook["title"])
        self.assertEquals("Amazing Author", firstBook["author"])
        self.assertEquals("1991", secondBook["year"])
        self.assertEquals("7654321", secondBook["isbn"])
        self.assertEquals("9999", secondBook["id"])

    def test_canUserAddReviewAndRatingForBook_calledWithExistingRating_returnFalse(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = [{"rating": 4, "review": "Lovely story."}]
        self.mockDB.execute.return_value = self.mockFetchResult

        canAddReview = self.databaseHandler.canUserAddReviewAndRatingForBook("1234", "9999")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with(
            "SELECT rating, review FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
            {"user_id": "1234", "book_id": "9999"})

        self.assertFalse(canAddReview)

    def test_addBookReview_correctSqlIsExecuted(self):
        self.databaseHandler.addBookReviewAndRating(5, "This is a great book.", "1234", "9999")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with(
            "INSERT INTO reviews (user_id, book_id, rating, review) VALUES (:user_id, :book_id, :rating, :review)",
            {"user_id": "1234", "book_id": "9999", "rating": 5, "review": "This is a great book."})

        self.mockDB.commit.assert_called_once()

    def test_retrieveCurrentUsersReviewAndRatingOfBook_correctSqlIsExecuted(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = {"rating": 4, "review": "It is a lovely book."}
        self.mockDB.execute.return_value = self.mockFetchResult

        reviewAndRating = self.databaseHandler.retrieveCurrentUsersReviewAndRatingOfBook("9999", "1234")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with(
            "SELECT rating, review FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
            {"user_id": "1234", "book_id": "9999"})

        self.assertEquals("It is a lovely book.", reviewAndRating["review"])
        self.assertEquals(4, reviewAndRating["rating"])

    def test_retrieveAllRatingsForBook(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchall.return_value = [{"rating": 1}, {"rating": 2}, {"rating": 3}, {"rating": 4},
                                                      {"rating": 5}]
        self.mockDB.execute.return_value = self.mockFetchResult

        ratings = self.databaseHandler.retrieveAllRatingsForBook("9999")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT rating FROM reviews WHERE book_id = :book_id",
                                               {"book_id": "9999"})

        self.assertEquals([1, 2, 3, 4, 5], ratings)


if __name__ == '__main__':
    unittest.main()
