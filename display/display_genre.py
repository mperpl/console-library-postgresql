from sqlalchemy import text

def display_genre(engine, genre_id):
    # Display:
    #   Id
    #   Genre

    query = "SELECT id, name FROM genres WHERE id = :genre_id;"
    try:
        with engine.begin() as con:
            query_result = con.execute(text(query), {'genre_id': genre_id}).fetchone()

            if query_result:
                print(f"{query_result[1]} (id: {query_result[0]})")
            else: print('No genre data')
            
            print("\ndisplay_genre ran\n")
    except Exception as e:
        print('Error during display_genre: ', e)