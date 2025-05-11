from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import psycopg2
from app.database.get_connection_string import get_connection_string
import logging


# Настройка логгера
logger = logging.getLogger(__name__)

# Получение строки для подключения к PostgreSQL
connection_string = get_connection_string()

# Создание движка
engine = create_engine(
    connection_string,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# Создание фабрики сессий
Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    """
    Контекстный менеджер для работы с сессией базы данных.
    Автоматически коммитит изменения при успешном выполнении 
    и откатывает при возникновении исключений.
    """
    session = Session()
    try:
        yield session
        session.commit()
        
    except Exception as err:
        session.rollback()
        logger.error(f"Database error: {err}")
        raise err
    
    finally:
        session.close()
