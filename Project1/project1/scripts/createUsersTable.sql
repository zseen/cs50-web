CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    hashedpassword VARCHAR NOT NULL,
);