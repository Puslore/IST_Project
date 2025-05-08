# Файл, описывающий сессию с базой данных
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('')
Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
        
    except Exception as err:
        session.rollback()
        raise err
    
    finally:
        session.close()
