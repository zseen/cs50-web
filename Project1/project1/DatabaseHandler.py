from unittest.mock import Mock
from unittest import TestCase
import unittest


class DatabaseHandler:
    def __init__(self, database):
        self._database = database

    def registerUser(self, username, hashedPassword):
        self._database.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                               {"username": username,
                                "hash": hashedPassword})
        self._database.commit()

    def retrieveUserData(self, username):
        hashedPasswordAndId = self._database.execute("SELECT hash, id FROM users WHERE username = :username",
                                                     {"username": username}).fetchall()

        if not hashedPasswordAndId:
            raise ValueError("No data found for this username")

        return hashedPasswordAndId

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
        self.dbh.registerUser("Abc", "a1b2c3")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                               {'username': 'Abc', 'hash': 'a1b2c3'})
        self.mockDB.commit.assert_called_once()

    def test_retrieveUserData_idAndHashedPasswordReturned(self):
        self.mockFetchAllResult = Mock()
        self.mockFetchAllResult.fetchall.return_value = {"id": "4", "hash": "a1b2c3"}
        self.mockDB.execute.return_value = self.mockFetchAllResult

        userData = self.dbh.retrieveUserData("Abc")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT hash, id FROM users WHERE username = :username",
                                               {'username': 'Abc'})

        self.assertEquals("4", userData["id"])
        self.assertEquals("a1b2c3", userData["hash"])

    def test_retrieveUserData_notExistingUserRaiseException(self):
        self.mockFetchAllResult = Mock()
        self.mockFetchAllResult.fetchall.return_value = {}
        self.mockDB.execute.return_value = self.mockFetchAllResult

        with self.assertRaises(ValueError):
            self.dbh.retrieveUserData("Abc")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT hash, id FROM users WHERE username = :username",
                                               {'username': 'Abc'})

    def test_IsUsernameTaken_returnTrue(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = {"username": "Abc"}
        self.mockDB.execute.return_value = self.mockFetchResult

        result = self.dbh.isUsernameTaken("Abc")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT username FROM users WHERE username = :username",
                                               {'username': 'Abc'})

        self.assertTrue(result)

    def testRetrieveBookData(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = "123"
        self.mockDB.execute.return_value = self.mockFetchResult

        result = self.dbh.retrieveBookData("123")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT title, author, year FROM books WHERE isbn = :isbn",
                                               {"isbn": "123"})

        self.assertEquals(result, "123")


if __name__ == '__main__':
    unittest.main()
