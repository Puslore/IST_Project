from app.database.session import get_session
from app.database.repositories.admin_repository import AdminRepository
from app.database.repositories.user_repository import UserRepository
from app.database.repositories.publication_repository import PublicationRepository
from app.database.repositories.publisher_repository import PublisherRepository
from app.database.repositories.show_item_repository import ShowItemRepository
from app.database.repositories.courier_repository import CourierRepository
from app.database.repositories.complaint_repository import ComplaintRepository
from app.database.repositories.delivery_repository import DeliveryRepository


class AdminController:
    def __init__(self):
        self.session = None
        self._init_repositories()
    
    def _init_repositories(self):
        """Инициализация репозиториев"""
        with get_session() as session:
            self.session = session
            self.admin_repo = AdminRepository(session)
            self.user_repo = UserRepository(session)
            self.publication_repo = PublicationRepository(session)
            self.publisher_repo = PublisherRepository(session)
            self.show_item_repo = ShowItemRepository(session)
            self.courier_repo = CourierRepository(session)
            self.complaint_repo = ComplaintRepository(session)
            self.delivery_repo = DeliveryRepository(session)
    
    def authenticate_admin(self, phone_number, password):
        """
        Аутентификация администратора
        
        Args:
            phone_number (str): Номер телефона
            password (str): Пароль
            
        Returns:
            Admin: Объект администратора при успешной аутентификации, None при ошибке
        """
        try:
            return self.admin_repo.authenticate(phone_number, password)
        except Exception as err:
            print(f"Ошибка аутентификации: {err}")
            return None
    
    def create_admin(self, admin_data):
        """
        Создает нового администратора
        
        Args:
            admin_data (dict): Данные администратора
            
        Returns:
            tuple: (success, admin_object или error_message)
        """
        try:
            admin = self.admin_repo.create_admin(admin_data)
            if not admin:
                return False, "Ошибка создания администратора"
            return True, admin
        except Exception as err:
            print(f"Ошибка создания администратора: {err}")
            return False, str(err)
    
    def get_table_data(self, table_name):
        """
        Получает данные для указанной таблицы
        
        Args:
            table_name (str): Название таблицы
            
        Returns:
            tuple: (headers, data)
        """
        try:
            if table_name == "Пользователи":
                users = self.user_repo.get_all().all()
                headers = ["ID", "Имя", "Фамилия", "Телефон", "Email", "Адрес", "Дата регистрации", "Активен"]
                data = [
                    (u.id, u.first_name, u.last_name, u.phone_number, 
                     u.email, u.address, u.registration_date, u.is_active)
                    for u in users
                ]
                return headers, data
            elif table_name == "Администраторы":
                admins = self.admin_repo.get_all().all()
                headers = ["ID", "Имя", "Фамилия", "Телефон", "Email", "Зарплата", "Активен"]
                data = [
                    (a.id, a.first_name, a.last_name, a.phone_number, 
                     a.email, a.salary, a.is_active)
                    for a in admins
                ]
                return headers, data
            elif table_name == "Издательства":
                publishers = self.publisher_repo.get_all().all()
                headers = ["ID", "Название", "Владелец", "Дата начала продаж", "Активен"]
                data = [
                    (p.id, p.name, p.owner, p.sales_start, p.is_active)
                    for p in publishers
                ]
                return headers, data
            elif table_name == "Публикации":
                publications = self.publication_repo.get_all().all()
                headers = ["ID", "Название", "Тип", "Издательство", "В продаже"]
                data = [
                    (p.id, p.name, p.publication_type, p.publisher.name if p.publisher else "Нет", p.on_sale)
                    for p in publications
                ]
                return headers, data
            elif table_name == "Выпуски":
                show_items = self.show_item_repo.get_all().all()
                headers = ["ID", "Название", "Номер", "Тип", "Издание", "Цена", "В продаже"]
                data = [
                    (s.id, s.name, s.issue_number, s.publication_type, 
                     s.publication_series.name if s.publication_series else "Нет", s.cost, s.on_sale)
                    for s in show_items
                ]
                return headers, data
            elif table_name == "Доставщики":
                couriers = self.courier_repo.get_all().all()
                headers = ["ID", "Имя", "Фамилия", "Зарплата", "Рейтинг", "Активен"]
                data = [
                    (c.id, c.first_name, c.last_name, c.salary, c.rating, c.is_active)
                    for c in couriers
                ]
                return headers, data
            elif table_name == "Жалобы":
                complaints = self.complaint_repo.get_all().all()
                headers = ["ID", "Доставщик", "Описание", "Дата"]
                data = [
                    (c.id, f"{c.courier.first_name} {c.courier.last_name}" if c.courier else "Нет", 
                     c.description, c.created_at)
                    for c in complaints
                ]
                return headers, data
            elif table_name == "Доставки":
                deliveries = self.delivery_repo.get_all().all()
                headers = ["ID", "Тип", "Получатель", "Адрес", "Стоимость", "Доставлено"]
                data = [
                    (d.id, d.item_type, d.recipient_name, d.recipient_address, 
                     d.item_cost, d.is_delivered)
                    for d in deliveries
                ]
                return headers, data
            else:
                return [], []
        except Exception as err:
            print(f"Ошибка получения данных таблицы: {err}")
            return [], []
    
    def get_publishers(self):
        """
        Получает список издателей
        
        Returns:
            list: Список активных издателей
        """
        try:
            return self.publisher_repo.get_active_publishers()
        except Exception as err:
            print(f"Ошибка получения издателей: {err}")
            return []
    
    def get_publications(self):
        """
        Получает список публикаций
        
        Returns:
            list: Список активных публикаций
        """
        try:
            return self.publication_repo.get_all().filter_by(on_sale=True).all()
        except Exception as err:
            print(f"Ошибка получения публикаций: {err}")
            return []
    
    def get_publication_type(self, publication_id):
        """
        Получает тип публикации по ID
        
        Args:
            publication_id (int): ID публикации
            
        Returns:
            str: Тип публикации
        """
        try:
            publication = self.publication_repo.find_by_id(publication_id)
            return publication.publication_type if publication else None
        except Exception as err:
            print(f"Ошибка получения типа публикации: {err}")
            return None
    
    def create_publication(self, publication_data):
        """
        Создает новое издание
        
        Args:
            publication_data (dict): Данные издания
            
        Returns:
            tuple: (success, publication_object или error_message)
        """
        try:
            publication = self.publication_repo.create_publication(publication_data)
            if not publication:
                return False, "Ошибка создания издания"
            return True, publication
        except Exception as err:
            print(f"Ошибка создания издания: {err}")
            return False, str(err)
    
    def create_issue(self, issue_data):
        """
        Создает новый выпуск
        
        Args:
            issue_data (dict): Данные выпуска
            
        Returns:
            tuple: (success, issue_object или error_message)
        """
        try:
            issue = self.show_item_repo.create_show_item(issue_data)
            if not issue:
                return False, "Ошибка создания выпуска"
            return True, issue
        except Exception as err:
            print(f"Ошибка создания выпуска: {err}")
            return False, str(err)
