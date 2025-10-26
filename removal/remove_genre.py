from sqlalchemy import text
from helpers.validate_genre_id import validate_genre_id
from helpers.confirm import confirm

def remove_genre(engine):
    genre_id = validate_genre_id(engine)

    genres_remove_query = 'DELETE FROM genres WHERE id = :genre_id;'
    confirmed = confirm('\nAre you sure you want to delete the genre? (y/n): ')
    if confirmed:
        try:
            with engine.begin() as con:
                genres_remove_query_result = con.execute(text(genres_remove_query), {'genre_id': genre_id})
                if genres_remove_query_result.rowcount > 0: print('removed the genre')
                else: print('removal operation failed')
        except Exception as e:
            print('[ERROR] remove_genre', e)
    else:
        print('operation aborted')