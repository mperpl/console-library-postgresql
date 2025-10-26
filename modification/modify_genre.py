from sqlalchemy import text
from helpers.validate_genre_id import validate_genre_id
from display.display_genres import display_genres
from display.display_genre import display_genre

def modify_genre(engine):
    # pick an id
    # display current data
    # ask if change is needed
    display_genres(engine)

    genre_id = validate_genre_id(engine)

    genres_update_query = 'UPDATE genres SET name = :name WHERE id = :genre_id;'
    try:
        with engine.begin() as con:
            name = input('Change the value to: ').strip('').lower()
            genres_update_query_result = con.execute(text(genres_update_query), {'name': name, 'genre_id': genre_id})
            if genres_update_query_result.rowcount > 0: print('modified the genre')
            else: print('modification operation failed')
    except Exception as e:
        print('[ERROR] modify_genre', e)

    if genre_id: display_genre(engine, genre_id)
