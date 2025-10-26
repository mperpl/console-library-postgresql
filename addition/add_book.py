from sqlalchemy import text
from display.display_genres import display_genres
from helpers.validate_year import validate_year
from helpers.validate_author_id import validate_author_id
from helpers.confirm import confirm

def add_book(engine):
    
    # authors_select_query = "SELECT first_name, last_name FROM authors WHERE id = :id;"
    
    genres_select_query = "SELECT name FROM genres WHERE id = :id;"
    books_insert_query = "INSERT INTO books (title, release_year, description, author_id) VALUES (:title, :release_year, :description, :author_id) RETURNING id;"
    book_copies_insert_query = "INSERT INTO book_copies (book_id) VALUES (:book_id);"
    book_genres_insert_query = "INSERT INTO book_genres (book_id, genre_id) VALUES (:book_id, :genre_id);"

    try:
        while True:
            title = input('Title: ').strip()
            if len(title) > 0:
                break
            else: 
                print("Error: Title cannot be empty.")

        release_year = validate_year('Year: ')

        description = input('Description: ').strip()

        book_count = 0
        while True:
            try:
                book_count = int(input('Number of Copies: '))
                if book_count > 0:
                    break
                else:
                    print("Error: Number of Copies must be greater than 0.")
            except ValueError: 
                print('Error: Number of Copies must be an integer! Try again.')

        author_id = validate_author_id(engine)

        display_genres(engine)
        genre_id_list = []
        with engine.connect() as con: 
            while True:
                try:
                    genre_id_input = input('Genre ID (-1 to finish): ').strip()
                    if genre_id_input == '-1':
                        break
                    
                    genre_id = int(genre_id_input)
                    genres_select_query_result = con.execute(text(genres_select_query), {'id': genre_id}).fetchone()
                    if genres_select_query_result:
                        genre_name = genres_select_query_result[0]
                        if genre_id not in genre_id_list:
                            genre_id_list.append(genre_id)
                            print(f'"{genre_name}" added to the book.')
                        else:
                            print(f'Genre ID {genre_id} has already been added.')
                    else:
                        print('Error: No genre found with this ID.')
                except ValueError: 
                    print('Error: Genre ID must be an integer! Try again.')
        
        if not genre_id_list:
            print("\nWarning: No genre was selected.")

        confirmed = confirm('\nDo you want to proceed and save the data? (y/n): ')
        if confirmed:
            try:
                with engine.begin() as con:
                    books_insert_query_result = con.execute(text(books_insert_query), {
                        'title': title, 
                        'release_year': release_year, 
                        'description': description, 
                        'author_id': author_id
                    }).fetchone()
                    
                    book_id = None
                    if books_insert_query_result:
                        book_id = books_insert_query_result[0]
                        print(f'\n[SUCCESS] Book added (ID: {book_id}).')
                    else:
                         print("[ERROR] Failed to retrieve the ID of the new book.")
                         return

                    for _ in range(book_count):
                        con.execute(text(book_copies_insert_query), {'book_id': book_id})
                    print(f'[SUCCESS] Added {book_count} copies.')

                    for genre_id in genre_id_list:
                        con.execute(text(book_genres_insert_query), {'book_id': book_id, 'genre_id': genre_id})
                    print(f'[SUCCESS] Added {len(genre_id_list)} genre links.')
                

            except Exception as e:
                print(f'An error occurred during data write: {e}')
        else:
            print('Operation canceled.')
            return

    except Exception as e:
        print(f'Global error in add book wizard: {e}')
