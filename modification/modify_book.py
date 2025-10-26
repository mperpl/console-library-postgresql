from sqlalchemy import text
from helpers.validate_book_id import validate_book_id
from helpers.validate_author_id import validate_author_id
from helpers.validate_year import validate_year
from helpers.validate_genre_id import validate_genre_id
from helpers.validate_int import validate_int
from display.display_book import display_book
from display.display_authors_short import display_authors_short
from display.display_genres import display_genres

def modify_book(engine):
    # pick an id
    # display current data
    # ask if change is needed

    book_id = validate_book_id(engine)

    genre_id = None
    old_genre_id = None
    params = None
    books_update_query = None
    fields_to_update = {}
    add_count = 0

    def get_title():
        return input('Updated title: ').strip()
    
    def get_description():
        return input('Updated description: ').strip()
    
    def get_author():
        display_authors_short(engine)
        return validate_author_id(engine, 'Updated author id: ')

    while True:
        answer = input('\nWhat do you want to update (title(t), author(a), release_year(ry), genre(g), description(d), count(c) leave empty to exit: ').strip().lower()
        possible_answers = {
            ('title', 't'): ('title', get_title),
            ('release_year', 'ry', 'r', 'y'): ('release_year', validate_year),
            ('description', 'd', 'desc'): ('description', get_description),
            ('author', 'a', 'name'): ('author', get_author),
            ('count', 'c', 'amount', 'copies', 'copy'): ('count', validate_int)
        }
        if not answer: break
        else:
            for keys, (field, func) in possible_answers.items():
                if answer in keys:
                    if field == 'count':
                        add_count = func('How many copies to add / delete')
                        break
                    else: fields_to_update[field] = func()
            else:
                if answer in ('genre', 'genres', 'g', 'gen'):
                    while True:
                        answer = input('do you want to assign or deassign a new genre?(1/2)').strip().lower()
                        if not answer:
                            print('Improper input. Try again.')
                        else: break

                    if answer == '1':
                        display_genres(engine)
                        genre_id = validate_genre_id(engine)

                    elif answer == '2':
                        old_genre_id = validate_genre_id(engine)

    try:
        if fields_to_update:
            update_fields_list = [f"{key} = :{key}" for key in fields_to_update.keys()]
            books_update_query = f"UPDATE books SET {', '.join(update_fields_list)} WHERE id = :book_id"
            params = {**fields_to_update, 'book_id': book_id}
        book_genres_insert_query = 'INSERT INTO book_genres (book_id, genre_id) VALUES (:book_id, :genre_id) ON CONFLICT DO NOTHING;'
        book_genres_delete_query = 'DELETE FROM book_genres WHERE genre_id = :old_genre_id AND book_id = :book_id'
        book_copies_insert_query = 'INSERT INTO book_copies (book_id) VALUES (:book_id);'
        
        with engine.begin() as con:

            if add_count > 0:
                copies_to_add = [{'book_id': book_id} for _ in range(add_count)]
                book_copies_insert_query_result = con.execute(text(book_copies_insert_query), copies_to_add)
                if book_copies_insert_query_result.rowcount == add_count: 
                    print(f'Successfully added {add_count} copies.')
                else: 
                    print('Error while attempting to add a copy.')

            if add_count < 0:
                # TODO
                # copies_to_add = [{'book_id': book_id} for _ in range(add_count)]
                # book_copies_insert_query_result = con.execute(text(book_copies_insert_query), copies_to_add)
                # if book_copies_insert_query_result.rowcount == add_count: 
                #     print(f'Successfully added {add_count} copies.')
                # else: 
                #     print('Error while attempting to add a copy.')
                pass

            if fields_to_update:
                books_update_query_result = con.execute(text(books_update_query), params)
                if books_update_query_result.rowcount > 0: print('updated the book')
                else: print('modification operation failed')
                
            if genre_id:
                book_genres_insert_query_result = con.execute(text(book_genres_insert_query), {'book_id': book_id, 'genre_id': genre_id})
                if book_genres_insert_query_result.rowcount > 0: print('updated the book')
                else: print('modification operation failed')

            if old_genre_id:
                book_genres_delete_query_result = con.execute(text(book_genres_delete_query), {'old_genre_id': old_genre_id, 'book_id': book_id})
                if book_genres_delete_query_result.rowcount > 0: print('updated the book')
                else: print('modification operation failed')
    except Exception as e:
        print('[ERROR] modify_book', e)

    if book_id: display_book(engine, book_id)