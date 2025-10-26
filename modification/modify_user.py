from sqlalchemy import text
from helpers.validate_user_id import validate_user_id
from helpers.validate_name import validate_name
from helpers.validate_past_date import validate_past_date
from helpers.validate_phone_number import validate_phone_number
from helpers.validate_email import validate_email
from display.display_user import display_user

def modify_user(engine):
    user_id = validate_user_id(engine)
    display_user(engine, user_id)

    update_map = {
        ('f', 'fn', 'first_name', 'first', 'name'): ('first_name', validate_name, 'Updated first name: '),
        ('l', 'ln', 'last_name', 'last'): ('last_name', validate_name, 'Updated last name: '),
        ('b', 'bd', 'birth', 'birth_date', 'date'): ('birth_date', validate_past_date, 'Updated birth date: '),
        ('ph', 'pn', 'phone', 'phone_number'): ('phone_number', validate_phone_number, 'Updated phone number: '),
        ('e', 'email', 'mail'): ('email', validate_email, 'Updated email: ')
    }

    fields_to_update = {}

    while True:
        answer = input('\nWhat do you want to update (first_name(fn), last_name(ln), birth_date(bd), phone_number(pn), email(e))? Leave empty to exit: ').strip().lower()
        if not answer:
            break
        for keys, (field, validator, prompt) in update_map.items():
            if answer in keys:
                fields_to_update[field] = validator(prompt)
                break
        else:
            print('Invalid input')

    if not fields_to_update:
        print('No changes made.')
        return

    update_clause = ', '.join(f"{key} = :{key}" for key in fields_to_update)
    query = text(f"UPDATE users SET {update_clause} WHERE id = :user_id")
    params = {**fields_to_update, 'user_id': user_id}

    try:
        with engine.begin() as con:
            result = con.execute(query, params)
            if result.rowcount > 0:
                print('User updated successfully.')
            else:
                print('Update failed or no rows affected.')
    except Exception as e:
        print(f'[ERROR] modify_user: {e}')

    display_user(engine, user_id)