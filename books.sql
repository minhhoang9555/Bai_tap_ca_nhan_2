CREATE TABLE books (
 id SERIAL PRIMARY KEY,
 title VARCHAR(255) NOT NULL,
 author VARCHAR(255) NOT NULL,
 year INTEGER NOT NULL,
 genre VARCHAR(100) NOT NULL
);
