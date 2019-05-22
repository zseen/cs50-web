from unittest.mock import Mock
from unittest import TestCase
import unittest


class DatabaseHandler:
    def __init__(self, database):
        self._database = database

    def registerUser(self, username, hashedPassword):
        self._database.execute("INSERT INTO users (username, hashed_password) VALUES(:username, :hashed_password)",
                               {"username": username,
                                "hashed_password": hashedPassword})
        self._database.commit()

    def retrieveUserData(self, username):
        hashedPasswordAndId = self._database.execute("SELECT hashed_password, id FROM users WHERE username = :username",
                                                     {"username": username}).fetchall()

        if not hashedPasswordAndId:
            return None

        numRows = sum(1 for _ in hashedPasswordAndId)
        if numRows > 1:
            return "Unexpected error: multiple users exist with username"

        return hashedPasswordAndId[0]

    def isUsernameTaken(self, username):
        preExistingUsername = self._database.execute("SELECT username FROM users WHERE username = :username",
                                                     {"username": username}).fetchone()

        return preExistingUsername is not None

    def retrieveBookData(self, isbn):
        book = self._database.execute("SELECT title, author, year, isbn FROM books WHERE isbn = :isbn",
                                      {"isbn": isbn}).fetchone()
        return book


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

    def test_retrieveUserData_idAndhashedPasswordReturned(self):
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

    def test_isUsernameTaken_returnTrue(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = [{"username": "Bookworm45"}]
        self.mockDB.execute.return_value = self.mockFetchResult

        isTaken = self.databaseHandler.isUsernameTaken("Bookworm45")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT username FROM users WHERE username = :username",
                                               {'username': 'Bookworm45'})

        self.assertTrue(isTaken)

    def test_retrieveBookData_allDataReturnedByISBN(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = {"title": "ThisGoodBook", "author": "Amazing Author",
                                                      "year": "2012", "isbn": "1234567"}
        self.mockDB.execute.return_value = self.mockFetchResult

        bookData = self.databaseHandler.retrieveBookData("1234567")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT title, author, year, isbn FROM books WHERE isbn = :isbn",
                                               {"isbn": "1234567"})

        self.assertEquals("ThisGoodBook", bookData["title"])
        self.assertEquals("Amazing Author", bookData["author"])
        self.assertEquals("2012", bookData["year"])
        self.assertEquals("1234567", bookData["isbn"])


if __name__ == '__main__':
    unittest.main()
