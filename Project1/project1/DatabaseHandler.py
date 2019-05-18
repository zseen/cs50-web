from unittest.mock import *
from unittest import TestCase
import unittest


class DatabaseHandler:
    def __init__(self, database):
        self.database = database

    def insertUsernameAndHashIntoUsers(self, username, hashedPW):
        self.database.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                   {"username": username,
                    "hash": hashedPW})
        self.database.commit()

    def selectHashAndIdByUsernameFromUsers(self, username):
        hashedPw = self.database.execute("SELECT hash, id FROM users WHERE username = :username",
                          {"username": username}).fetchall()
        return hashedPw

    def isUsernameAvailable(self, username):
        isa = self.database.execute("SELECT username FROM users WHERE username = :username",
                        {"username": username}).fetchall()

        return len(isa) == 0

    def selectTitleAuthorYearByISBNFromBooks(self, isbn):
        book = self.database.execute("SELECT title, author, year FROM books WHERE isbn = :isbn",
                                     {"isbn": isbn}).fetchone()
        return book


class MockTestDatabaseHandler(TestCase):
    def setUp(self):
        self.mockDB = Mock()
        self.dbh = DatabaseHandler(self.mockDB)

    def testInsertion(self):
        self.dbh.insertUsernameAndHashIntoUsers("Abc", "9d56")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                               {'username': 'Abc', 'hash': '9d56'})
        self.mockDB.commit.assert_called_once()

    def testSelectHash(self):
        self.mockFetchAllResult = Mock()
        self.mockFetchAllResult.fetchall.return_value = "985747"
        self.mockDB.execute.return_value = self.mockFetchAllResult

        pw = self.dbh.selectHashAndIdByUsernameFromUsers("asd")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT hash, id FROM users WHERE username = :username",
                                          {"username": 'asd'})

        self.assertEquals("985747", pw)

if __name__ == '__main__':
    unittest.main()

