from .db_config import engine
from .migrate_book_data import migrate_book_data
from .migrate_people_data import migrate_people_data
from .create_database_tables import create_database_tables
from .insert_sample_data import insert_sample_data

create_database_tables(engine)
insert_sample_data(engine, True)
migrate_book_data(engine)
migrate_people_data(engine)