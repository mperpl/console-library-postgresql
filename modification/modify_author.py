from sqlalchemy import text
from helpers.validate_author_id import validate_author_id
from helpers.validate_name import validate_name
from helpers.validate_year import validate_year
from display.display_author import display_author


def modify_author(engine):
    author_id = validate_author_id(engine)
    
    possible_answers = {
        ('f', 'fn', 'first_name', 'first', 'name'): ('first_name', validate_name, 'First Name: '),
        ('l', 'ln', 'last_name', 'last'): ('last_name', validate_name, 'Last Name: '),
        ('by', 'birth', 'birth_year', 'year'): ('birth_year', validate_year, 'Birth Year: '),
        ('d', 'dy', 'death', 'death_date'): ('death_year', validate_year, 'Death Year: ')
    }

    fields_to_update = {}
    while True:
        answer = input('\nWhat do you want to update (first_name(fn), last_name(ln), birth_year(by), death_year(dy))? Leave empty to exit: ').strip().lower()
        if not answer: return
        else:
            for keys, (field, func, prompt) in possible_answers.items():
                if answer in keys:
                    fields_to_update[field] = func(prompt)
                    break
        try:
            if fields_to_update:
                update_fields_list = [f"{key} = :{key}" for key in fields_to_update.keys()]
                authors_update_query = f"UPDATE authors SET {', '.join(update_fields_list)} WHERE id = :author_id"
                params = {**fields_to_update, 'author_id': author_id}

            with engine.begin() as con:
                if fields_to_update:
                    books_update_query_result = con.execute(text(authors_update_query), params)
                    if books_update_query_result.rowcount > 0: print('updated the author')
                    else: print('modification operation failed')
        except Exception as e:
            print('[ERROR] modify_book', e)

        if author_id: display_author(engine, author_id)