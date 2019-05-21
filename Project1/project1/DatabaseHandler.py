from unittest.mock import Mock
from unittest import TestCase
import unittest


class DatabaseHandler:
    def __init__(self, database):
        self._database = database

    def registerUser(self, username, hashedpassword):
        self._database.execute("INSERT INTO users (username, hashedpassword) VALUES(:username, :hashedpassword)",
                               {"username": username,
                                "hashedpassword": hashedpassword})
        self._database.commit()

    def retrieveUserData(self, username):
        hashedpasswordAndId = self._database.execute("SELECT hashedpassword, id FROM users WHERE username = :username",
                                                     {"username": username}).fetchall()

        if not hashedpasswordAndId:
            return None

        if sum(1 for _ in hashedpasswordAndId) > 1:
            return "Something went wrong."

        return hashedpasswordAndId[0]

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
        self.dbh.registerUser("Bookworm45", "pkdf43ep91qa")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("INSERT INTO users (username, hashedpassword) VALUES(:username, :hashedpassword)",
                                               {'username': 'Bookworm45', 'hashedpassword': 'pkdf43ep91qa'})
        self.mockDB.commit.assert_called_once()

    def test_retrieveUserData_idAndhashedpasswordReturned(self):
        self.mockFetchAllResult = Mock()
        self.mockFetchAllResult.fetchall.return_value = [{"hashedpassword": "pkdf43ep91qa", "id": 4}]
        self.mockDB.execute.return_value = self.mockFetchAllResult

        userData = self.dbh.retrieveUserData("Bookworm45")
        print(userData)

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT hashedpassword, id FROM users WHERE username = :username",
                                               {'username': 'Bookworm45'})

        self.assertEquals(4, userData["id"])
        self.assertEquals("pkdf43ep91qa", userData["hashedpassword"])

    def test_retrieveUserData_notExistingUserReturnNone(self):
        self.mockFetchAllResult = Mock()
        self.mockFetchAllResult.fetchall.return_value = []
        self.mockDB.execute.return_value = self.mockFetchAllResult

        userData = self.dbh.retrieveUserData("Bookworm45")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT hashedpassword, id FROM users WHERE username = :username",
                                               {'username': 'Bookworm45'})

        self.assertEquals(userData, None)

    def test_isUsernameTaken_returnTrue(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = [("Bookworm45")]
        self.mockDB.execute.return_value = self.mockFetchResult

        result = self.dbh.isUsernameTaken("Bookworm45")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT username FROM users WHERE username = :username",
                                               {'username': 'Bookworm45'})

        self.assertTrue(result)

    def test_retrieveBookData_allDataReturnedByISBN(self):
        self.mockFetchResult = Mock()
        self.mockFetchResult.fetchone.return_value = ("ThisGoodBook", "Amazing Author", "2012", "1234567")
        self.mockDB.execute.return_value = self.mockFetchResult

        result = self.dbh.retrieveBookData("1234567")

        self.mockDB.execute.assert_called_once()
        self.mockDB.execute.assert_called_with("SELECT title, author, year, isbn FROM books WHERE isbn = :isbn",
                                               {"isbn": "1234567"})

        self.assertEquals(result[0], "ThisGoodBook")
        self.assertEquals(result[1], "Amazing Author")
        self.assertEquals(result[2], "2012")
        self.assertEquals(result[3], "1234567")



if __name__ == '__main__':
    unittest.main()
