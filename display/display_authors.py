from sqlalchemy import text

def display_authors(engine):
    # Display:
    #   Id
    #   Name
    #   Birth Year
    #   Death Year
    #   Books

    query = """
        SELECT a.id, a.first_name, a.last_name, a.birth_year, a.death_year, STRING_AGG(b.title, ', ')
        FROM Authors a LEFT JOIN Books b ON a.id = b.author_id
        GROUP BY a.id
        ORDER BY first_name, last_name DESC;"""
    try:
        with engine.begin() as con:
            query_result = con.execute(text(query)).fetchall()

            if query_result:
                for result in query_result:
                    print(f"""
    ID: {result[0]}
    Name: {result[1]} {result[2]}
    Birth Year: {result[3] or '-'}
    Death Year: {result[4] or '-'}
    Books: {result[5] or '-'}
    """,end='')
            else: print('No authors data')
            
            print("\ndisplay_authors ran\n")
    except Exception as e:
        print('Error during display_authors: ', e)