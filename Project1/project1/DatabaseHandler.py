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

        rows = sum(1 for _ in hashedPasswordAndId)
        if rows > 1:
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
        self.dbh = DatabaseHandler(self.mockDB)

    def test_registerUser_correctSqlIsExecuted(self):
        self.dbh.registerUser("Bookworm45", "adf43ef91ba")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with(
            "INSERT INTO users (username, hashed_password) VALUES(:username, :hashed_password)",
            {'username': 'Bookworm45', 'hashed_password': 'adf43ef91ba'})
        self.mockDB.commit.assert_called_once()

    def test_retrieveUserData_idAndhashedPasswordReturned(self):
        self.mockFetchAllResult = Mock()
        self.mockFetchAllResult.fetchall.return_value = [{"hashed_password": "adf43ef91ba", "id": 4}]
        self.mockDB.execute.return_value = self.mockFetchAllResult

        userData = self.dbh.retrieveUserData("Bookworm45")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT hashed_password, id FROM users WHERE username = :username",
                                               {'username': 'Bookworm45'})

        self.assertEquals(4, userData["id"])
        self.assertEquals("adf43ef91ba", userData["hashed_password"])

    def test_retrieveUserData_notExistingUserReturnNone(self):
        self.mockFetchAllResult = Mock()
        self.mockFetchAllResult.fetchall.return_value = None
        self.mockDB.execute.return_value = self.mockFetchAllResult

        userData = self.dbh.retrieveUserData("Bookworm45")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT hashed_password, id FROM users WHERE username = :username",
                                               {'username': 'Bookworm45'})

        self.assertEquals(userData, None)

    def test_isUsernameTaken_returnTrue(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = [{"username": "Bookworm45"}]
        self.mockDB.execute.return_value = self.mockFetchResult

        result = self.dbh.isUsernameTaken("Bookworm45")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT username FROM users WHERE username = :username",
                                               {'username': 'Bookworm45'})

        self.assertTrue(result)

    def test_retrieveBookData_allDataReturnedByISBN(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = {"title": "ThisGoodBook", "author": "Amazing Author",
                                                      "year": "2012", "isbn": "1234567"}
        self.mockDB.execute.return_value = self.mockFetchResult

        result = self.dbh.retrieveBookData("1234567")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT title, author, year, isbn FROM books WHERE isbn = :isbn",
                                               {"isbn": "1234567"})

        self.assertEquals(result["title"], "ThisGoodBook")
        self.assertEquals(result["author"], "Amazing Author")
        self.assertEquals(result["year"], "2012")
        self.assertEquals(result["isbn"], "1234567")


if __name__ == '__main__':
    unittest.main()
