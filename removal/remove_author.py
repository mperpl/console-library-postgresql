from sqlalchemy import text
from helpers.validate_author_id import validate_author_id
from helpers.confirm import confirm

def remove_author(engine):
    author_id = validate_author_id(engine)

    authors_remove_query = 'DELETE FROM authors WHERE id = :author_id;'
    confirmed = confirm('\nAre you sure you want to delete the author and everything they are connected with like books, loans and so on? (y/n): ')
    if confirmed:
        try:
            with engine.begin() as con:
                authors_remove_query_result = con.execute(text(authors_remove_query), {'author_id': author_id})
                if authors_remove_query_result.rowcount > 0: print('removed the author')
                else: print('removal operation failed')
        except Exception as e:
            print('[ERROR] remove_author', e)
    else:
        print('operation aborted')