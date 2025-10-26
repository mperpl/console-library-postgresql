from sqlalchemy import text

def display_users(engine):
    # Display:
    #   Id
    #   Name
    #   Birth date
    #   Age
    #   Phone number
    #   Email
    #   Loans

    query = """
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.birth_date,
            DATE_PART('year', AGE(CURRENT_DATE, u.birth_date)),
            u.phone_number,
            u.email,
            STRING_AGG(b.title, ', ')
        FROM users u
            LEFT JOIN loans l ON u.id = l.user_id
            LEFT JOIN book_copies bc ON l.book_copy_id = bc.id
            LEFT JOIN books b ON bc.book_id = b.id
        GROUP BY u.id
        ORDER BY
            last_name,
            first_name DESC;"""
    try:
        with engine.begin() as con:
            query_result = con.execute(text(query)).fetchall()

            if query_result:
                print()
                for result in query_result:
                    print(f"""\
    ID: {result[0]}
    Name: {result[1]} {result[2]}
    Birth Date: {result[3] or '-'}
    Age: {result[4] or '-'}
    Phone Number: {result[5] or '-'}
    Email: {result[6] or '-'}
    Loans: {result[7] or '-'}
    """)
            else: print('No user data')
            
            print("display_users ran\n")
    except Exception as e:
        print('Error during display_users: ', e)