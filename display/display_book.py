from sqlalchemy import text

def display_book(engine, book_id):
    # Display:
    #   Id
    #   Title
    #   Author
    #   Genres
    #   Release Year
    #   Number of Copies
    #   Description

    query = """
        WITH total_copies AS (
            SELECT book_id, COUNT(*) AS total
            FROM book_copies
            GROUP BY book_id
        ),
        loans_count AS (
            SELECT bc.book_id, COUNT(l.book_copy_id) AS on_loan
            FROM book_copies bc
            LEFT JOIN loans l ON bc.id = l.book_copy_id
            GROUP BY bc.book_id
        )
        SELECT
            b.id,
            b.title,
            a.id as author_id,
            a.first_name,
            a.last_name,
            STRING_AGG(DISTINCT g.name, ', ') AS genres,
            b.release_year,
            COALESCE(tc.total, 0) - COALESCE(lc.on_loan, 0) AS available_copies,
            b.description
        FROM books b
            LEFT JOIN authors a ON b.author_id = a.id
            LEFT JOIN book_genres bg ON b.id = bg.book_id
            LEFT JOIN genres g ON g.id = bg.genre_id
            LEFT JOIN total_copies tc ON b.id = tc.book_id
            LEFT JOIN loans_count lc ON b.id = lc.book_id
        WHERE b.id = :book_id
        GROUP BY b.id, a.id, a.first_name, a.last_name, b.title, b.release_year, tc.total, lc.on_loan;"""
    try:
        with engine.begin() as con:
            query_result = con.execute(text(query), {'book_id': book_id}).fetchall()

            if query_result:
                for result in query_result:
                    print(f"""
    Title: {result[1]}; ID: {result[0]}
    Author: {result[3]} {result[4]}; ID: {result[2]}
    Genres: {result[5] or '-'}
    Release Date: {result[6] or '-'}
    Available Copies: {result[7] or '0'}
    Description: {result[8] or '-'}
    """,end='')
            else: print('No book data')
            
            print("\ndisplay_book ran\n")
    except Exception as e:
        print('Error during display_book: ', e)