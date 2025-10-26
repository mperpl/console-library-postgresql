from sqlalchemy import text
from helpers.validate_int import validate_int
from display.display_author import display_author
from helpers.confirm import confirm

def validate_author_id(engine):
    while True:
        author_id = validate_int('Author ID: ')
        authors_select_query = "SELECT id FROM authors WHERE id = :author_id;"

        try:
            with engine.begin() as con:
                authors_select_query_result = con.execute(text(authors_select_query), {'author_id': author_id}).fetchone()
                if authors_select_query_result:
                    display_author(engine, author_id)
                    confirmed = confirm('Is this the author? (y/n)')
                    if confirmed:
                        return author_id
                else: print('author with such id not found')
        except Exception as e:
            print('[ERROR] during validate_author_id: ', e)