from sqlalchemy import text
from helpers.validate_int import validate_int
from helpers.confirm import confirm
from display.display_genre import display_genre

def validate_genre_id(engine):
    while True:
        genre_id = validate_int('Genre ID: ')
        genres_select_query = "SELECT id FROM genres WHERE id = :genre_id;"

        try:
            with engine.begin() as con:
                genres_select_query_result = con.execute(text(genres_select_query), {'genre_id': genre_id}).fetchone()
                if genres_select_query_result:
                    display_genre(engine, genre_id)
                    confirmed = confirm('Is this the genre? (y/n): ')
                    if confirmed: return genre_id
                else: print('genre with such id not found')
        except Exception as e:
            print('[ERROR] during validate_genre_id: ', e)