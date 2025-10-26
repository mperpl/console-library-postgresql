from sqlalchemy import text

def insert_sample_data(engine, insert_data: bool):
    if insert_data:
        try:
            with engine.begin() as con:

                con.execute(text("""
                    -- Wstawianie danych do tabeli genres
                    INSERT INTO genres (name) VALUES
                    ('fantasy'),
                    ('horror'),
                    ('sci-fi'),
                    ('thriller'),
                    ('classic'),
                    ('comedy'),
                    ('mystery'),
                    ('dystopian'),
                    ('psychological'),
                    ('adventure'),
                    ('romance'),
                    ('historical'),
                    ('tragedy'),
                    ('coming-of-age'),
                    ('epic')
                    ON CONFLICT (name) DO NOTHING;"""))

                con.execute(text("""
                    -- Wstawianie danych do tabeli authors
                    INSERT INTO authors (first_name, last_name, birth_year, death_year) VALUES
                    ('Stephen', 'King', 1947, NULL),
                    ('J.R.R.', 'Tolkien', 1892, 1973),
                    ('George', 'Orwell', 1903, 1950),
                    ('Agatha', 'Christie', 1890, 1976),
                    ('Stanisław', 'Lem', 1921, 2006)
                    ON CONFLICT DO NOTHING;"""))
                            
                con.execute(text("""
                    -- Wstawianie danych do tabeli users
                    INSERT INTO users (first_name, last_name, birth_date, phone_number, email) VALUES
                    ('Anna', 'Kowalska', '1990-05-15', '501-123-456', 'anna.k@example.com'),
                    ('Jan', 'Nowak', '1985-11-20', '602-234-567', 'jan.n@example.com'),
                    ('Piotr', 'Wiśniewski', '1992-02-10', NULL, 'piotr.w@example.com'),
                    ('Magda', 'Lewandowska', '1998-07-22', '703-345-678', 'magda.l@example.com')
                    ON CONFLICT DO NOTHING;"""))

                con.execute(text("""
                    -- Wstawianie danych do tabeli books
                    INSERT INTO books (title, author_id, release_year, description) VALUES
                    ('The Shining', (SELECT id FROM authors WHERE last_name = 'King'), 1977, 'A family spends the winter in an isolated hotel where an evil spiritual presence influences the father into violence.'),
                    ('The Hobbit', (SELECT id FROM authors WHERE last_name = 'Tolkien'), 1937, 'A fantasy novel by English author J. R. R. Tolkien.'),
                    ('Nineteen Eighty-Four', (SELECT id FROM authors WHERE last_name = 'Orwell'), 1949, 'A dystopian social science fiction novel and cautionary tale.'),
                    ('Murder on the Orient Express', (SELECT id FROM authors WHERE last_name = 'Christie'), 1934, 'A detective novel by Agatha Christie.'),
                    ('Solaris', (SELECT id FROM authors WHERE last_name = 'Lem'), 1961, 'A science fiction novel by Polish author Stanisław Lem.')
                    ON CONFLICT DO NOTHING;"""))
        
                con.execute(text("""
                    INSERT INTO book_copies (book_id)
                    SELECT b.id
                    FROM (VALUES
                        ('The Shining'), ('The Shining'),
                        ('The Hobbit'), ('The Hobbit'),
                        ('Nineteen Eighty-Four'), ('Nineteen Eighty-Four'),
                        ('Murder on the Orient Express'),
                        ('Solaris'), ('Solaris')
                    ) AS titles(title_to_insert)
                    JOIN books b ON b.title = titles.title_to_insert;
                """))

                con.execute(text("""
                    -- Wstawianie danych do tabeli book_genres
                    INSERT INTO book_genres (book_id, genre_id) VALUES
                    ((SELECT id FROM books WHERE title = 'The Shining'), (SELECT id FROM genres WHERE name = 'horror')),
                    ((SELECT id FROM books WHERE title = 'The Shining'), (SELECT id FROM genres WHERE name = 'thriller')),
                    ((SELECT id FROM books WHERE title = 'The Hobbit'), (SELECT id FROM genres WHERE name = 'fantasy')),
                    ((SELECT id FROM books WHERE title = 'The Hobbit'), (SELECT id FROM genres WHERE name = 'classic')),
                    ((SELECT id FROM books WHERE title = 'Nineteen Eighty-Four'), (SELECT id FROM genres WHERE name = 'sci-fi')),
                    ((SELECT id FROM books WHERE title = 'Nineteen Eighty-Four'), (SELECT id FROM genres WHERE name = 'classic')),
                    ((SELECT id FROM books WHERE title = 'Murder on the Orient Express'), (SELECT id FROM genres WHERE name = 'thriller')),
                    ((SELECT id FROM books WHERE title = 'Solaris'), (SELECT id FROM genres WHERE name = 'sci-fi'))
                    ON CONFLICT DO NOTHING;"""))
                                
                con.execute(text("""
                    -- Wstawianie danych do tabeli loans
                    -- Teraz odwołujemy się do konkretnych kopii książek
                    INSERT INTO loans (user_id, book_copy_id, loan_date) VALUES
                    ((SELECT id FROM users WHERE email = 'anna.k@example.com'), (SELECT id FROM book_copies WHERE book_id = (SELECT id FROM books WHERE title = 'The Shining') LIMIT 1), '2025-08-01'),
                    ((SELECT id FROM users WHERE email = 'jan.n@example.com'), (SELECT id FROM book_copies WHERE book_id = (SELECT id FROM books WHERE title = 'The Hobbit') LIMIT 1), '2025-07-20'),
                    ((SELECT id FROM users WHERE email = 'anna.k@example.com'), (SELECT id FROM book_copies WHERE book_id = (SELECT id FROM books WHERE title = 'Murder on the Orient Express') LIMIT 1 OFFSET 1), '2025-08-10'),
                    ((SELECT id FROM users WHERE email = 'piotr.w@example.com'), (SELECT id FROM book_copies WHERE book_id = (SELECT id FROM books WHERE title = 'Nineteen Eighty-Four') LIMIT 1), '2025-08-20'),
                    ((SELECT id FROM users WHERE email = 'magda.l@example.com'), (SELECT id FROM book_copies WHERE book_id = (SELECT id FROM books WHERE title = 'Solaris') LIMIT 1), '2025-08-25');"""))
                
            print("data inserted succesfully")
        except Exception as e:
            print("Error while handling PostgreSQL:", e)