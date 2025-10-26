from sqlalchemy import text
from helpers.validate_book_id import validate_book_id
from helpers.confirm import confirm

def remove_book(engine):
    book_id = validate_book_id(engine)

    books_remove_query = 'DELETE FROM books WHERE id = :book_id;'
    confirmed = confirm('\nAre you sure you want to delete the book? (y/n): ')
    if confirmed:
        try:
            with engine.begin() as con:
                books_remove_query_result = con.execute(text(books_remove_query), {'book_id': book_id})
                if books_remove_query_result.rowcount > 0: print('removed the book')
                else: print('removal operation failed')
        except Exception as e:
            print('[ERROR] remove_book', e)
    else:
        print('operation aborted')