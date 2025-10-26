from sqlalchemy import text
from helpers.validate_genre import validate_genre

def add_genre(engine):
    genre = validate_genre('Genre: ')

    genre_select_query = 'SELECT id FROM genres WHERE name = :genre;'
    genre_insert_query = 'INSERT INTO genres (name) VALUES (:genre) RETURNING id;'

    try:
        with engine.begin() as con:

            while True:
                genre_select_query_result = con.execute(text(genre_select_query), {'genre': genre}).fetchone()
                if genre_select_query_result:
                    print(f'Genre already exists (id: {genre_select_query_result[0]})')
                    genre = validate_genre('Genre: ')
                else: break

            genre_insert_query_result = con.execute(text(genre_insert_query), {'genre': genre}).fetchone()
            if genre_insert_query_result:
                new_id = genre_insert_query_result[0]
                print('New genre with an ID of: ', new_id)
            else: print('Couldn\'t add genre and retrive it\'s id')

    except Exception as e:
        print(f"[ERROR] {e}")
        