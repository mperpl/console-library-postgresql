from sqlalchemy import text

def display_user(engine, user_id):
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
            DATE_PART('year', AGE(CURRENT_DATE, u.birth_date)) as age,
            u.phone_number,
            u.email,
            STRING_AGG(b.title, ', ')
        FROM users u
            LEFT JOIN loans l ON u.id = l.user_id
            LEFT JOIN book_copies bc ON l.book_copy_id = bc.id
            LEFT JOIN books b ON bc.book_id = b.id
        WHERE u.id = :user_id
        GROUP BY u.id"""
    try:
        with engine.begin() as con:
            query_result = con.execute(text(query), {'user_id': user_id}).fetchone()

            if query_result:
                print(f"""
    ID: {query_result[0]}
    Name: {query_result[1]} {query_result[2]}
    Birth Date: {query_result[3] or '-'}
    Age: {query_result[4] or '-'}
    Phone Number: {query_result[5] or '-'}
    Email: {query_result[6] or '-'}
    Loans: {query_result[7] or '-'}
    """)
            else: print('No user data')
            
            print("display_user ran\n")
    except Exception as e:
        print('Error during display_user: ', e)