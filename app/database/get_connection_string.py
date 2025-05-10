import os
from dotenv import load_dotenv


load_dotenv()

USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
DATABASE = os.environ["DATABASE"]

def get_connection_string() -> str:
    '''Возвращает строку для подключения PostgreSQL'''
    return f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'