from sqlalchemy import text
from helpers.validate_email import validate_email
from helpers.validate_phone_number import validate_phone_number
from helpers.validate_past_date import validate_past_date
from helpers.validate_name import validate_name

def add_user(engine):
    first_name = validate_name('First Name: ')
    last_name = validate_name('Last Name: ')
    birth_date = validate_past_date('Birthday: ')
    phone_number = validate_phone_number('Phone Number like 00 000 000 000 (no spaces): ')
    email = validate_email('Email (email@mail.com): ')
    
    with engine.begin() as con:
        users_insert_query = "INSERT INTO users (first_name, last_name, birth_date, phone_number, email) VALUES(:first_name, :last_name, :birth_date, :phone_number, :email) RETURNING id;"
        try:
            users_insert_query_result = con.execute(text(users_insert_query), {'first_name': first_name, 'last_name': last_name, 'birth_date': birth_date, 'phone_number': phone_number, 'email': email}).fetchone()
            new_user_id = users_insert_query_result[0]

            print(f'User added successfully. Their id is {new_user_id}')
        except Exception as e:
            print('[ERROR] while adding user', e)