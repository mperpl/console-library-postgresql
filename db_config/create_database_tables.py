from sqlalchemy import text

def create_database_tables(engine):
    try:
        with engine.begin() as con:
            con.execute(text("""
                CREATE TABLE IF NOT EXISTS genres (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL);"""))

            con.execute(text("""
                CREATE TABLE IF NOT EXISTS authors (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    birth_year INT,
                    death_year INT,
                    UNIQUE (first_name, last_name));"""))

            con.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    birth_date DATE,
                    phone_number VARCHAR(15),
                    email VARCHAR(50),
                    UNIQUE (first_name, last_name, phone_number));"""))

            con.execute(text("""
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    release_year INT,
                    description VARCHAR(255),
                    author_id INT,
                    UNIQUE(title, author_id),
                    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE);"""))

            con.execute(text("""
                CREATE TABLE IF NOT EXISTS book_genres (
                    book_id INT,
                    genre_id INT,
                    PRIMARY KEY (book_id, genre_id),
                    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
                    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE);"""))

            con.execute(text("""
                CREATE TABLE IF NOT EXISTS book_copies (
                    id SERIAL PRIMARY KEY,
                    book_id INT NOT NULL,
                    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE);"""))
            
            con.execute(text("""
                CREATE TABLE IF NOT EXISTS loans (
                    id SERIAL PRIMARY KEY,
                    user_id INT,
                    book_copy_id INT,
                    loan_date DATE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (book_copy_id) REFERENCES book_copies(id) ON DELETE CASCADE
                );"""))
            
            print("tables created succesfully")
    except Exception as e:
        print("Error while handling PostgreSQL:", e)