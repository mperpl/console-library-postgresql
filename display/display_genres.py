from sqlalchemy import text

def display_genres(engine):
    # Display:
    #   Id
    #   Genre

    query = """
        SELECT id, name FROM genres ORDER BY name DESC;"""
    try:
        with engine.begin() as con:
            query_result = con.execute(text(query)).fetchall()

            if query_result:
                for result in query_result:
                    print(f"{result[1]} (id: {result[0]})")
            else: print('No genre data')
            
            print("\ndisplay_genres ran\n")
    except Exception as e:
        print('Error during display_genres: ', e)