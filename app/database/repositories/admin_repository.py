from . import BaseRepository
from app.database.models import Admin

class AdminRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Admin, session)
    
    def create_admin(self, data: dict) -> Admin | None:
        '''
        Создает нового администратора
        
        Arguments:
            data (dict): Словарь с данными администратора, содержащий:
                first_name (str): Имя администратора
                last_name (str): Фамилия администратора
                phone_number (str): Номер телефона
                address (str): Адрес
                salary (float): Зарплата администратора
                password (str): Пароль администратора
                email (str, optional): Email администратора
                middle_name (str, optional): Отчество администратора
        
        Returns:
            Admin: Созданный администратор при успешной регистрации, None при ошибке
        '''
        try:
            # Проверка существования администратора с таким телефоном
            existing_admin = self.session.query(self.model_class).filter(
                self.model_class.phone_number == data['phone_number']
            ).first()
            
            if existing_admin:
                raise ValueError("Администратор с таким телефоном уже существует")
            
            # Создание нового администратора
            new_admin = Admin(
                first_name=data['first_name'],
                last_name=data['last_name'],
                middle_name=data.get('middle_name'),
                email=data.get('email'),
                phone_number=data['phone_number'],
                address=data['address'],
                salary=data['salary']
            )
            
            # Установка пароля
            new_admin.set_password(data['password'])
            
            # Добавление администратора в БД
            self.add(new_admin)
            
            # Коммит изменений
            if not self.commit():
                return None
            
            return new_admin
            
        except Exception as err:
            print(f"Ошибка создания администратора: {err}")
            return None
    
    def authenticate(self, phone_number: str, password: str) -> Admin | None:
        '''
        Аутентификация администратора по телефону и паролю
        
        Arguments:
            phone_number (str): Номер телефона
            password (str): Пароль
        
        Returns:
            Admin: Объект администратора при успешной аутентификации, None при ошибке
        '''
        try:
            admin = self.session.query(self.model_class).filter_by(
                phone_number=phone_number,
                is_active=True
            ).first()
            
            if admin and admin.verify_password(password):
                return admin
            
            return None
            
        except Exception as err:
            print(f"Ошибка аутентификации: {err}")
            return None
