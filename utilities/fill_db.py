import csv
from datetime import datetime
from app.database.models import User, Publication, Publisher, Issue
from app.database.repositories import UserRepository, PublicationRepository, PublisherRepository, IssueRepository
from app.database.session import get_session
from .csv_operations import read_csv
import random


def fill_db():
    """
    Заполняет базу данных тестовыми данными из CSV файлов
    """
    # Пути к CSV файлам
    users_csv = './utilities/test_data/users_sample.csv'
    publications_csv = './utilities/test_data/publications_sample.csv'
    publishers_csv = './utilities/test_data/publishers_sample.csv'
    show_items_csv = './utilities/test_data/show_items_sample.csv'

    # Функция для чтения CSV с заголовками

    # Чтение данных из CSV файлов
    users_data = read_csv(users_csv)
    publications_data = read_csv(publications_csv)
    publishers_data = read_csv(publishers_csv)
    show_items_data = read_csv(show_items_csv)

    # Создание сессии и репозиториев
    with get_session() as session:
        user_repo = UserRepository(session)
        publication_repo = PublicationRepository(session)
        publisher_repo = PublisherRepository(session)
        show_item_repo = Issue(session)

        # Добавление издательств
        for pub_data in publishers_data:
            # Обработка первого столбца с BOM-маркером
            name_key = next(key for key in pub_data.keys() if 'name' in key)
            
            publisher = Publisher(
                name=pub_data[name_key],
                owner=pub_data['owner'],
                is_active=pub_data['is_active'].lower() == 'true',
                sales_start=datetime.strptime(pub_data['sales_start'], '%Y-%m-%d %H:%M:%S.%f')
            )
            publisher_repo.add(publisher)
        publisher_repo.commit()
        print("Издательства добавлены в БД")

        # Добавление публикаций
        for pub_data in publications_data:
            # Обработка первого столбца с BOM-маркером
            pub_type_key = next(key for key in pub_data.keys() if 'publication_type' in key)
            
            publication = Publication(
                publication_type=pub_data[pub_type_key],
                publisher_id=int(pub_data['publisher_id']),
                on_sale=pub_data['on_sale'].lower() == 'true',
                sales_start=datetime.strptime(pub_data['sales_start'], '%Y-%m-%d %H:%M:%S'),
                name=random.choice([pub_data['name'], 'журнал']),
                description=pub_data['description']
            )
            publication_repo.add(publication)
        publication_repo.commit()
        print("Публикации добавлены в БД")

        # Добавление пользователей
        for user_data in users_data:
            # Обработка первого столбца с BOM-маркером
            first_name_key = next(key for key in user_data.keys() if 'first_name' in key)
            
            user = User(
                first_name=user_data[first_name_key],
                last_name=user_data['last_name'],
                middle_name=user_data['middle_name'] if user_data['middle_name'] else None,
                phone_number=user_data['phone_number'],
                email=user_data['email'] if user_data['email'] else None,
                address=user_data['address'],
                tg_chat_id=None,  # В CSV может быть пустое значение
                ad_consent=user_data['ad_consent'].lower() == 'true',
                registration_date=datetime.strptime(user_data['registration_date'], '%Y-%m-%d %H:%M:%S.%f'),
                is_active=user_data['is_active'].lower() == 'true'
            )
            user_repo.add(user)
        user_repo.commit()
        print("Пользователи добавлены в БД")

        # Добавление выпусков
        for item_data in show_items_data:
            # Обработка первого столбца с BOM-маркером
            issue_number_key = next(key for key in item_data.keys() if 'issue_number' in key)
            
            show_item = Issue(
                issue_number=int(item_data[issue_number_key]),
                issue_date=datetime.strptime(item_data['issue_date'], '%Y-%m-%d %H:%M:%S'),
                is_special_edition=item_data['is_special_edition'].lower() == 'true',
                publication_type=item_data['publication_type'],
                publication_series_id=int(item_data['publication_series_id']),
                on_sale=item_data['on_sale'].lower() == 'true',
                name=item_data['name'],
                description=item_data['description'],
                pg=int(float(item_data['pg'])) if item_data['pg'] else None,
                cost=float(item_data['cost']) if item_data['cost'] else None,
                discount=item_data['is_discount'].lower() == 'true' if item_data['is_discount'] else False
            )
            show_item_repo.add(show_item)
        show_item_repo.commit()
        print("Выпуски добавлены в БД")

    print('Данные успешно загружены в базу данных')
