import csv
import os
import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


parser = argparse.ArgumentParser()
parser.add_argument("-f", "-csvFile")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    args = parser.parse_args()

    f = open(args.f)
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book with {isbn}, {title}, {author}, {year}.")
    db.commit()


if __name__ == "__main__":
    main()
