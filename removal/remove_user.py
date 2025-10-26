from sqlalchemy import text
from helpers.validate_user_id import validate_user_id
from helpers.confirm import confirm

def remove_user(engine):
    user_id = validate_user_id(engine)

    users_remove_query = 'DELETE FROM users WHERE id = :user_id;'
    confirmed = confirm('\nAre you sure you want to delete the user and everything they are connected with like books, loans and so on? (y/n): ')
    if confirmed:
        try:
            with engine.begin() as con:
                users_remove_query_result = con.execute(text(users_remove_query), {'user_id': user_id})
                if users_remove_query_result.rowcount > 0: print('removed the user')
                else: print('removal operation failed')
        except Exception as e:
            print('[ERROR] remove_user', e)
    else:
        print('operation aborted')