from app.database.models.base_model import Base
from app.database.session import engine
from app.database.models import User, Publication, Publisher, Issue, Admin, Complaint, Courier, Delivery

def init_db():
    """Создает все таблицы в базе данных"""
    print("Создание таблиц базы данных...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы!")
