class DatabaseHandlerHelper:
    def __init__(self):
        pass

    @staticmethod
    def convertSqlRowsToList(rows, column):
        dataList = []
        for data in rows:
            dataList.append(data[column])

        return dataList