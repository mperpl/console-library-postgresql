from sqlalchemy import text

def display_books(engine):
    # Display:
    #   Id
    #   Title
    #   Author
    #   Genres
    #   Release Year
    #   Number of Copies

    # WITH total_copies AS (
    #     SELECT book_id, COUNT(*) AS total
    #     FROM book_copies
    #     GROUP BY book_id
    # ),
    # loans_count AS (
    #     SELECT bc.book_id, COUNT(l.book_copy_id) AS on_loan
    #     FROM book_copies bc
    #     LEFT JOIN loans l ON bc.id = l.book_copy_id
    #     GROUP BY bc.book_id
    # )
    # SELECT
    #     b.id,
    #     b.title,
    #     a.first_name,
    #     a.last_name,
    #     STRING_AGG(DISTINCT g.name, ', ') AS genres,
    #     b.release_year,
    #     COALESCE(tc.total, 0) - COALESCE(lc.on_loan, 0) AS available_copies,
    #     COALESCE(tc.total, 0) as total_copies
    # FROM books b
    # LEFT JOIN authors a ON b.author_id = a.id
    # LEFT JOIN book_genres bg ON b.id = bg.book_id
    # LEFT JOIN genres g ON g.id = bg.genre_id
    # LEFT JOIN total_copies tc ON b.id = tc.book_id
    # LEFT JOIN loans_count lc ON b.id = lc.book_id
    # GROUP BY b.id, a.first_name, a.last_name, b.title, b.release_year, tc.total, lc.on_loan
    # ORDER BY b.title;

    # query = """
    #     WITH total_copies AS (
    #         -- Liczy wszystkie fizyczne egzemplarze danej książki (total)
    #         SELECT book_id, COUNT(id) AS total
    #         FROM book_copies
    #         GROUP BY book_id
    #     ),
    #     active_loans AS (
    #         -- Liczy aktywne wypożyczenia, łącząc loans z egzemplarzami
    #         SELECT 
    #             bc.book_id, 
    #             COUNT(l.id) AS on_loan
    #         FROM book_copies bc
    #         -- Używamy INNER JOIN, aby wybrać tylko te book_copies, które mają aktywny wpis w loans.
    #         -- (Ponieważ loans przechowuje tylko aktywne wypożyczenia, INNER JOIN jest kluczowy)
    #         INNER JOIN loans l ON bc.id = l.book_copy_id
    #         GROUP BY bc.book_id
    #     )
    #     SELECT
    #         b.id,
    #         b.title,
    #         a.first_name,
    #         a.last_name,
    #         COALESCE(STRING_AGG(DISTINCT g.name, ', '), '') AS genres, 
    #         b.release_year,
            
    #         -- available_copies = total_copies - on_loan
    #         COALESCE(tc.total, 0) - COALESCE(al.on_loan, 0) AS available_copies,
            
    #         -- total_copies
    #         COALESCE(tc.total, 0) as total_copies
            
    #     FROM books b
    #     LEFT JOIN authors a ON b.author_id = a.id
    #     LEFT JOIN book_genres bg ON b.id = bg.book_id
    #     LEFT JOIN genres g ON g.id = bg.genre_id
    #     LEFT JOIN total_copies tc ON b.id = tc.book_id
    #     -- Złączenie z aktywnymi wypożyczeniami (al)
    #     LEFT JOIN active_loans al ON b.id = al.book_id

    #     GROUP BY 
    #         b.id, a.first_name, a.last_name, b.title, b.release_year, tc.total, al.on_loan
    #     ORDER BY b.title;
    #     """
    
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
            a.first_name,
            a.last_name,
            STRING_AGG(DISTINCT g.name, ', ') AS genres,
            b.release_year,
            COALESCE(tc.total, 0) - COALESCE(lc.on_loan, 0) AS available_copies,
            COALESCE(tc.total, 0) as total_copies
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.id
        LEFT JOIN book_genres bg ON b.id = bg.book_id
        LEFT JOIN genres g ON g.id = bg.genre_id
        LEFT JOIN total_copies tc ON b.id = tc.book_id
        LEFT JOIN loans_count lc ON b.id = lc.book_id
        GROUP BY b.id, a.first_name, a.last_name, b.title, b.release_year, tc.total, lc.on_loan
        ORDER BY b.title;
        """
    try:
        with engine.begin() as con:
            query_result = con.execute(text(query)).fetchall()

            if query_result:
                for result in query_result:
                    print(f"""
    ID: {result[0]}
    Title: {result[1]}
    Author: {result[2]} {result[3]}
    Genres: {result[4] or '-'}
    Release Date: {result[5] or '-'}
    Available Copies: {result[6] or '0'} / {result[7] or '0'}
    """,end='')
            else: print('No book data')
            
            print("\ndisplay_books ran\n")
    except Exception as e:
        print('Error during display_books: ', e)