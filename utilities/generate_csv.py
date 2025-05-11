import pandas as pd
from datetime import datetime, timedelta
import random


# Генерация данных для 10 пользователей
num_users = 10

first_names = ['Иван', 'Мария', 'Алексей', 'Ольга', 'Дмитрий', 'Елена', 'Сергей', 'Наталья', 'Павел', 'Анна']
last_names = ['Иванов', 'Петрова', 'Сидоров', 'Кузнецова', 'Смирнов', 'Попова', 'Васильев', 'Морозова', 'Новиков', 'Федорова']

users = []

for i in range(1, num_users + 1):
    users.append({
        'first_name': first_names[i-1],
        'last_name': last_names[i-1],
        'middle_name': None if i % 3 == 0 else f'Отчество{i}',
        'phone_number': f'+7900555{i:04d}',
        'email': f'user{i}@example.com' if i % 2 == 0 else None,
        'address': f'ул. Примерная, д.{i}' if i% 2 == 0 else f'ул. неПримерная, д.{i}',
        'tg_chat_id': None,
        'ad_consent': bool(i % 2),
        'registration_date': datetime.now(),
        'is_active': True
    })

users_df = pd.DataFrame(users)
users_df.to_csv('users_sample.csv', index=False, encoding='utf-8-sig')



# Генерация данных для 7 издательств
num_publishers = 7

publisher_names = [
    'Издательство А', 'Издательство Б', 'Издательство В',
    'Издательство Г', 'Издательство Д', 'Издательство Е', 'Издательство Ж'
]
owners = [
    'Иванов Иван Иванович', 'Петрова Мария Сергеевна', 'Сидоров Алексей Николаевич',
    'Кузнецова Ольга Владимировна', 'Смирнов Дмитрий Алексеевич', 'Попова Елена Викторовна', 'Васильев Сергей Петрович'
]

publishers = []

for i in range(1, num_publishers + 1):
    publishers.append({
        'name': publisher_names[i-1],
        'owner': owners[i-1],
        'is_active': True,
        'sales_start': datetime.now()
    })

publishers_df = pd.DataFrame(publishers)
publishers_df.to_csv('publishers_sample.csv', index=False, encoding='utf-8-sig')



# Функция для генерации случайной даты в диапазоне
def random_date(start, end):
    delta = end - start
    int_delta = delta.days
    random_day = random.randrange(int_delta)
    return start + timedelta(days=random_day)

# Генерация данных
num_newspapers = 50
num_magazines = 50

start_date = datetime(2020, 1, 1)
end_date = datetime(2025, 5, 11)

newspapers = []
magazines = []

for i in range(1, num_newspapers + 1):
    newspapers.append({
        'publication_type': 'newspaper',
        'publisher_id': random.randint(1, 7),
        'on_sale': False if i % 10 == 0 else True,
        'sales_start': random_date(start_date, end_date).strftime('%Y-%m-%d %H:%M:%S'),
        'name': f'Газета {i}',
        'description': f'Описание газеты {i}',
    })

for i in range(num_newspapers + 1, num_magazines + 1):
    magazines.append({
        'publication_type': 'magazine',
        'publisher_id': random.randint(1, 7),
        'on_sale': False if i % 10 == 0 else True,
        'sales_start': random_date(start_date, end_date).strftime('%Y-%m-%d %H:%M:%S'),
        'name': f'Журнал {i - num_newspapers}',
        'description': f'Описание журнала {i - num_newspapers}',
    })

# Объединяем данные
publications = newspapers + magazines

# Создаем DataFrame
publications_df = pd.DataFrame(publications)

# Сохраняем в CSV
csv_filename = 'publications_sample.csv'
publications_df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
print(f"Файл {csv_filename} успешно создан")



# Функция для генерации случайной даты в диапазоне
def random_date(start, end):
    delta = end - start
    int_delta = delta.days
    random_day = random.randrange(int_delta)
    return start + timedelta(days=random_day)

num_issues = 200
start_date = datetime(2020, 1, 1)
end_date = datetime(2025, 5, 11)

issues = []

for i in range(1, num_issues + 1):
    # Учтем поля is_discount и discount из вашей модели
    is_discount = random.choice([True, False])
    discount_value = random.randint(5, 50) if is_discount else None
    
    issues.append({
        'issue_number': random.randint(1, 2000),
        'issue_date': random_date(start_date, end_date).strftime('%Y-%m-%d %H:%M:%S'),
        'is_special_edition': random.choice([True, False]),
        'publication_type': random.choice(['newspaper', 'magazine']),
        'publication_series_id': random.randint(1, 100),  # Соответствует ID публикаций
        'on_sale': random.choice([True, False]),
        'name': f'Выпуск {i}',
        'description': f'Описание выпуска {i}',
        'pg': random.choice([None, 6, 12, 16, 18]),
        'cost': round(random.uniform(10, 100), 2),
        'is_discount': is_discount,
        'discount': discount_value
    })

issues_df = pd.DataFrame(issues)
issues_df.to_csv('show_items_sample.csv', index=False, encoding='utf-8-sig')
