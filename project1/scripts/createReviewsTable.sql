CREATE TABLE reviews(
    id SERIAL PRIMARY KEY,
    review VARCHAR,
    rating INTEGER,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books
);