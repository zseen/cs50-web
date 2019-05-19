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
        return hashedPasswordAndId

    def isUsernameAvailable(self, username):
        isAvailable = self._database.execute("SELECT username FROM users WHERE username = :username",
                                     {"username": username}).fetchone()

        return len(isAvailable) == 0

    def retrieveBookData(self, isbn):
        book = self._database.execute("SELECT title, author, year FROM books WHERE isbn = :isbn",
                                      {"isbn": isbn}).fetchone()
        return book


class MockTestDatabaseHandler(TestCase):
    def setUp(self):
        self.mockDB = Mock()
        self.dbh = DatabaseHandler(self.mockDB)

    def testInsertion(self):
        self.dbh.registerUser("Abc", "123")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                               {'username': 'Abc', 'hash': '123'})
        self.mockDB.commit.assert_called_once()

    def testSelectHash(self):
        self.mockFetchAllResult = Mock()
        self.mockFetchAllResult.fetchall.return_value = "123"
        self.mockDB.execute.return_value = self.mockFetchAllResult

        hashedPassword = self.dbh.retrieveUserData("abc")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT hash, id FROM users WHERE username = :username",
                                          {'username': 'abc'})

        self.assertEquals("123", hashedPassword)

    def testIsUsernameAvailable(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = "False"
        self.mockDB.execute.return_value = self.mockFetchResult

        result = self.dbh.isUsernameAvailable("Abc")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT username FROM users WHERE username = :username",
                                     {'username': 'Abc'})

        self.assertEquals(result, False)

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

