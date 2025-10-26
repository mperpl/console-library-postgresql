from sqlalchemy import text
genre_mapping = {
    'science-fiction': 'sci-fi',
    'dystopia': 'dystopian',
    'classical': 'classic'
}

def migrate_book_data(engine):
    try:
        with engine.begin() as con:
            with open('./db_config/book_data.txt', 'r', encoding='utf-8') as data:
                lines = data.readlines()
                for line in lines:
                    split_line = line.split("|")

                    # get line data
                    title = split_line[0]
                    # get name
                    split_author_name = split_line[1].strip().split(" ")
                    first_name = split_author_name[0]
                    if len(split_author_name) > 1:
                        last_name = " ".join(split_author_name[1:])
                    else: last_name = ""
                    genres = split_line[2].split(",")
                    release_year = split_line[3]
                    count = int(split_line[4])

                    print("title:",title)
                    print("first_name:",first_name)
                    print("last_name:",last_name)
                    print("genres:",genres)
                    print("release_year:",release_year)
                    print("count:",count)


                    # add author
                    author_id = None
                    select_author = con.execute(text("""
                        SELECT id FROM authors WHERE first_name = :first_name AND last_name = :last_name;"""),
                        {'first_name': first_name, 'last_name': last_name}).fetchone()
                    
                    if(select_author):
                        author_id = select_author[0]
                    else:
                        insert_author = con.execute(text("""
                            INSERT INTO authors (first_name, last_name) VALUES (:first_name, :last_name) ON CONFLICT (first_name, last_name) DO NOTHING RETURNING id;"""),
                            {'first_name': first_name, 'last_name': last_name}).fetchone()
                        
                        if insert_author:
                            author_id = insert_author[0]
                        else:
                            select_existing_author = con.execute(text("""
                                SELECT id FROM authors WHERE first_name = :first_name AND last_name = :last_name;"""),
                                {'first_name': first_name, 'last_name': last_name}).fetchone()
                            author_id = select_existing_author[0]
                    print(f"Author '{split_line[1]}' ID: {author_id}")


                    # add book
                    book_id = None
                    if author_id:
                        select_book = con.execute(text("""
                            SELECT id FROM books WHERE title = :title"""),
                            {'title': title}).fetchone()
                        
                        if select_book:
                            book_id = select_book[0]
                        else:
                            book_insert = con.execute(text("""
                                INSERT INTO books (title, release_year, author_id) VALUES (:title, :release_year, :author_id) ON CONFLICT (title, author_id) DO NOTHING RETURNING id;"""),
                                {'title': title, 'release_year': release_year, 'author_id': author_id}).fetchone()
                            if book_insert:
                                book_id = book_insert[0]
                            else:
                                select_existing_book = con.execute(text("""
                                    SELECT id FROM books WHERE title = :title"""),
                                    {'title': title}).fetchone()
                                book_id = select_existing_book[0]
                    print(f"Book '{title}' ID: {book_id}")


                    # add book_copy
                    if book_id:
                        for _ in range(count):
                            con.execute(text("""
                                INSERT INTO book_copies (book_id) VALUES (:book_id);"""),
                            {'book_id': book_id})
                    print(f"Added {count} copies for '{title}'")
                    

                    # add genre
                    for genre in genres:

                        mapped_genre_name = genre_mapping.get(genre, genre).lower()
                        genre_id = None

                        select_genre = con.execute(text("""
                            SELECT id FROM genres WHERE name = :name;"""),
                            {'name': mapped_genre_name}).fetchone()
                        
                        if select_genre:
                            genre_id = select_genre[0]
                        else:
                            insert_genre = con.execute(text("""
                                INSERT INTO genres (name) VALUES (:name) ON CONFLICT (name) DO NOTHING RETURNING id;"""),
                                {'name': mapped_genre_name}).fetchone()
                            if insert_genre:
                                genre_id = insert_genre[0]
                            else:
                                select_genre = con.execute(text("""
                                    SELECT id FROM genres WHERE name = :name;"""),
                                    {'name': mapped_genre_name}).fetchone()
                                
                                genre_id = select_genre[0]

                        # add book_genre
                        if genre_id:
                            con.execute(text("""
                                INSERT INTO book_genres (book_id, genre_id) VALUES (:book_id, :genre_id) ON CONFLICT (book_id, genre_id) DO NOTHING;"""),
                                {'book_id': book_id, 'genre_id': genre_id})
                        print(f"Added genre '{mapped_genre_name}' to book '{title}'")



    except Exception as e:
        print("Error during migration:", e)