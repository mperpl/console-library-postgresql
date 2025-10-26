from sqlalchemy import text

def display_authors_short(engine):
    # Display:
    #   Id
    #   Name

    query = """
        SELECT id, first_name, last_name
        FROM Authors
        ORDER BY first_name, last_name DESC;"""
    try:
        with engine.begin() as con:
            query_result = con.execute(text(query)).fetchall()

            if query_result:
                for result in query_result:
                    print(f"ID: {result[0]} Name: {result[1]} {result[2]}")
            else: print('No authors data')
            
            print("\ndisplay_authors_short ran\n")
    except Exception as e:
        print('Error during display_authors_short: ', e)