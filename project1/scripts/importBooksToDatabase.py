import csv
import os
import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--csvFile")
    args = parser.parse_args()

    with open(args.csvFile) as csvFileHandle:
        reader = csv.reader(csvFileHandle)
        for isbn, title, author, year in reader:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                       {"isbn": isbn, "title": title, "author": author, "year": year})
            print(f"Added book with {isbn}, {title}, {author}, {year}.")
    db.commit()


if __name__ == "__main__":
    main()
