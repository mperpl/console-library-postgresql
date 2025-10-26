from sqlalchemy import text

def display_author(engine, author_id):
    # Display:
    #   Id
    #   Name
    #   Birth Year
    #   Death Year
    #   Books

    query = """
            SELECT a.id, a.first_name, a.last_name, a.birth_year, a.death_year, STRING_AGG(b.title, ', ')
            FROM Authors a LEFT JOIN Books b ON a.id = b.author_id
            WHERE a.id = :author_id
            GROUP BY a.id;
        """
    try:
        with engine.begin() as con:
            query_result = con.execute(text(query), {'author_id': author_id}).fetchone()

            if query_result:
                print(f"""
    ID: {query_result[0]}
    Name: {query_result[1]} {query_result[2]}
    Birth Year: {query_result[3] or '-'}
    Death Year: {query_result[4] or '-'}
    Books: {query_result[5] or '-'}""")
            else: print('No author\'s data')
            
            print("\ndisplay_author ran\n")
    except Exception as e:
        print('Error during display_author: ', e)