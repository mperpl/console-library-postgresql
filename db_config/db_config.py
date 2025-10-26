from sqlalchemy import create_engine
from .secret import password

DB_NAME = 'library'
DB_USER = 'postgres'
PORT = 5432
PASSWORD = password
HOST = 'localhost'

try:
    engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')
    print("Silnik bazy danych gotowy do użycia.")
except Exception as e:
    engine = None
    print(f"Błąd podczas tworzenia silnika bazy danych: {e}")
