from sqlalchemy import text
from helpers.validate_year import validate_year
from helpers.validate_name import validate_name

def add_author(engine):
    # Remember to modify users
    first_name = validate_name('First Name: ')
    last_name = validate_name('Last Name: ')
    while True:
        birth_year = validate_year('Birth Year: ')
        death_year = validate_year('Death Year: ')
        if birth_year < death_year: break
        else: print('Birth year can\'t be bigger than death year.')

    
    with engine.begin() as con:
        authors_insert_query = "INSERT INTO authors (first_name, last_name, birth_year, death_year) VALUES(:first_name, :last_name, :birth_year, :death_year) RETURNING id;"
        try:
            authors_insert_query_result = con.execute(text(authors_insert_query), {'first_name': first_name, 'last_name': last_name, 'birth_year': birth_year, 'death_year': death_year}).fetchone()
            new_author_id = authors_insert_query_result[0]

            print(f'Author added successfully. Their id is {new_author_id}')
        except Exception as e:
            print('[ERROR] while adding author', e)