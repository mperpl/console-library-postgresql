from sqlalchemy import text
from helpers.validate_user_id import validate_user_id
from helpers.validate_int import validate_int
from helpers.confirm import confirm

def return_book(engine):
    while True:
        user_id = validate_user_id(engine)
        if user_id: break

    select_query = """
        SELECT b.title, bc.id
        FROM users u
        JOIN loans l ON u.id = l.user_id
        JOIN book_copies bc ON bc.id = l.book_copy_id
        JOIN books b ON bc.book_id = b.id
        WHERE u.id = :user_id;"""
    
    delete_query = 'DELETE FROM loans WHERE user_id = :user_id AND book_copy_id = :book_copy_id'

    try:
        with engine.begin() as con:
            select_query_results = con.execute(text(select_query), {'user_id': user_id}).fetchall()
            if select_query_results:
                copies_list = []
                for result in select_query_results:
                    title, copy_id = result[0], result[1]
                    copies_list.append(copy_id)
                    print(f'{title} (id: {copy_id})')

                while True:
                    book_copy_id = validate_int('Book copy id to return: ')
                    if book_copy_id not in copies_list: print('no such copy id')
                    else: break

                confirmed = confirm('Are you sure you want to delete this entry? (y/n): ')
                if confirmed:
                    delete_query_result = con.execute(text(delete_query), {'user_id': user_id, 'book_copy_id': book_copy_id})
                    if delete_query_result.rowcount > 0: print('returned the book')
                    else: print('failed to return the book')
                else: print('operation aborted')

            else:
                print('User hasn\'t loaned any books yet')
    except Exception as e:
        print('Error during return_book: ', e)