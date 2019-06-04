def extractSingleRowValuese(rows, column):
    dataList = []
    for data in rows:
        dataList.append(data[column])

    return dataList