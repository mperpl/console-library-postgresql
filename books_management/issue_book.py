from sqlalchemy import text
from helpers.validate_book_id import validate_book_id
from helpers.validate_user_id import validate_user_id

def issue_book(engine):
    # find a book copy id thats not loaned
    # modify loans
    # TODO add mechanism to stop users from loaning the same book.

    select_copy_book_query = """
        SELECT bc.id
        FROM book_copies bc
        LEFT JOIN loans l ON bc.id = l.book_copy_id
        WHERE bc.book_id = :book_id AND l.id IS NULL
        LIMIT 1;"""

    loans_query = """
        INSERT INTO loans(user_id, book_copy_id, loan_date) VALUES(:user_id, :book_copy_id, CURRENT_DATE);"""
    
    book_id = validate_book_id(engine)
    user_id = validate_user_id(engine)

    try:
        with engine.begin() as con:

            book_copy_id = None
            select_copy_book_query_result = con.execute(text(select_copy_book_query), {'book_id': book_id}).fetchone()
            if select_copy_book_query_result:
                book_copy_id = select_copy_book_query_result[0]
            else:
                print(f"\nNo avalible copies of this book")
                return

            answer = input("ISSUE BOOK? (y\\n): ")
            answer = answer.lower().strip()

            if answer == "y":
                con.execute(text(loans_query), {'user_id': user_id, 'book_copy_id': book_copy_id})
                print('loans_query_result ran successfully')
            else:
                print('loans query NOT ran')

            print("\nissue_book ran\n")
    except Exception as e:
        print('Error during issue_book: ', e)