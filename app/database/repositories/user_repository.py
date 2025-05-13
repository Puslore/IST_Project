from . import BaseRepository
from app.database.models import User


class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(User, session)

    def registration(self, data: dict) -> User:
        '''
        Регистрирует нового пользователя в системе

        Arguments:
            data (dict): Словарь с данными пользователя, содержащий:
                first_name (str): Имя пользователя
                last_name (str): Фамилия пользователя
                email (str): Email пользователя
                phone_number (str): Номер телефона пользователя
                address (str): Адрес пользователя
                middle_name (str, optional): Отчество пользователя
                ad_consent (bool, optional): Согласие на получение рекламы

        Returns:
            User: Созданный пользователь при успешной регистрации, None при ошибке

        Raises:
            ValueError: Если пользователь с таким email или телефоном уже существует
        '''
        try:
            # Проверка существования пользователя с таким email или телефоном
            if data['email'] is not None:
                existing_user = self.session.query(self.model_class).filter(
                    (self.model_class.email == data['email']) | 
                    (self.model_class.phone_number == data['phone_number'])
                ).first()
            
            else:
                existing_user = self.session.query(self.model_class).filter(
                    (self.model_class.phone_number == data['phone_number'])
                ).first()

            if existing_user:
                raise ValueError("Пользователь с таким email или телефоном уже существует")

            # Создание нового пользователя
            new_user = User(
                first_name=data['first_name'],
                last_name=data['last_name'],
                middle_name=data.get('middle_name'),
                email=data.get('email'),
                phone_number=data['phone_number'],
                address=data['address'],
                ad_consent=data['ad_consent']
            )

            # Добавление пользователя в БД через метод базового класса
            self.add(new_user)
            
            # Коммит изменений
            if not self.commit():
                return None

            return new_user
            
        except Exception as err:
            print(f"Ошибка регистрации пользователя: {err}")
            return None

    def find_by_phone(self, phone_number):
        return self.session.query(self.model_class).filter_by(phone_number=phone_number).first()

    def get_active_subscriptions(self):
        return self.session.query(self.model_class).filter(
                        self.model_class.is_active == True,
                        self.model_class.subscribed_publications.any()
                    ).all()
