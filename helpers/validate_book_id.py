from sqlalchemy import text
from helpers.validate_int import validate_int
from display.display_book import display_book
from helpers.confirm import confirm

def validate_book_id(engine):
    while True:
        book_id = validate_int('Book ID: ')
        books_select_query = "SELECT id FROM books WHERE id = :book_id;"

        try:
            with engine.begin() as con:
                books_select_query_result = con.execute(text(books_select_query), {'book_id': book_id}).fetchone()
                if books_select_query_result:
                    display_book(engine, book_id)
                    confirmed = confirm('Is this the book? (y/n): ')
                    if confirmed: return book_id
                else: print('book with such id not found')
        except Exception as e:
            print('[ERROR] during validate_book_id: ', e)