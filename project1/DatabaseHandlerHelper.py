def extractSingleColumnValues(rows, columnName):
    extractedValues = []
    for row in rows:
        extractedValues.append(row[columnName])

    return extractedValues