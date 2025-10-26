from sqlalchemy import text

def get_author_books(engine, author_id):
    query = """
            SELECT a.id, a.first_name, a.last_name, b.id, b.title FROM authors a JOIN books b ON a.id = b.author_id WHERE a.id = :author_id;
        """
    try:
        with engine.begin() as con:
            query_result = con.execute(text(query), {'author_id': author_id}).fetchone()
            return query_result
    except Exception as e:
        print('Error during get_author_books: ', e)