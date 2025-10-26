from sqlalchemy import text
from helpers.validate_int import validate_int
from display.display_user import display_user
from helpers.confirm import confirm

def validate_user_id(engine):
    while True:
        user_id = validate_int('User ID: ')
        
        users_select_query = "SELECT first_name, last_name FROM users WHERE id = :user_id;"
        try:
            with engine.begin() as con:
                users_select_query_result = con.execute(text(users_select_query), {'user_id': user_id}).fetchone()
                if users_select_query_result:
                    display_user(engine, user_id)
                    confirmed = confirm('Is this the user? (y/n): ')
                    if confirmed: return user_id
                else: print('user with such id not found')
        except Exception as e:
            print('[ERROR] during validate_user_id: ', e)