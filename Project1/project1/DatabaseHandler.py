from unittest.mock import *


class DatabaseHandler:
    def __init__(self, database):
        self.database = database

    def insertUsernameAndHashIntoUsers(self, username, hash):
        self.database.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                   {"username": username,
                    "hash": hash})
        self.database.commit()

    def selectHashByUsernameFromUsers(self, username):
        hashedPw = self.database.execute("SELECT hash, id FROM users WHERE username = :username",
                          {"username": username}).fetchall()
        return hashedPw

    def isUsernameAvailable(self, username):
        isa = self.database.execute("SELECT username FROM users WHERE username = :username",
                        {"username": username}).fetchall()

        return len(isa) == 0



def testInsertion():
    mockDB = Mock()

    dbh = DatabaseHandler(mockDB)

    dbh.insertUsernameAndHashIntoUsers("Abc", "9d56")

    mockDB.execute.assert_called_once()
    mockDB.execute.assert_called_with("INSERT INTO users (username, hash) VALUES('abc', '9d56')")
    mockDB.commit.assert_called_once()

def testSelectHash():
    mockDB = Mock()

    dbh = DatabaseHandler(mockDB)

    mockDB.execute.assert_called_once()
    mockDB.execute.assert_called_with("SELECT hash FROM users WHERE username = 'asd'")

    mockFetchAllResult = Mock()
    mockFetchAllResult.fetchall.return_value("985747")
    mockDB.execute.return_value(mockFetchAllResult)

    pw = dbh.selectHashByUsernameFromUsers("abc")
    self.assertEquals("985747", pw)

