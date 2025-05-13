from datetime import datetime
from app.database.session import get_session
from app.database.repositories import (AdminRepository, UserRepository,
                                       PublicationRepository, PublisherRepository,
                                       ShowItemRepository, CourierRepository,
                                       ComplaintRepository, DeliveryRepository)

class AdminController:
    """Контроллер для администраторской панели"""
    
    def __init__(self):
        """Инициализирует контроллер и создает необходимые репозитории"""
        self.session = None
        self._init_repositories()
    
    def _init_repositories(self):
        """Инициализирует репозитории для работы с базой данных"""
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
    
    # --- Методы аутентификации и управления администраторами ---
    
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
            return True, admin
        except Exception as err:
            print(f"Ошибка создания администратора: {err}")
            return False, str(err)
    
    # --- Методы для получения данных таблиц ---
    
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
                    (p.id, p.name, p.publication_type, 
                     p.publisher.name if p.publisher else "Нет", p.on_sale)
                    for p in publications
                ]
                return headers, data
                
            elif table_name == "Выпуски":
                show_items = self.show_item_repo.get_all().all()
                headers = ["ID", "Название", "Номер", "Тип", "Издание", "Цена", "В продаже"]
                data = [
                    (s.id, s.name, s.issue_number, s.publication_type, 
                     s.publication_series.name if s.publication_series else "Нет", 
                     s.cost, s.on_sale)
                    for s in show_items
                ]
                return headers, data
                
            elif table_name == "Доставщики":
                couriers = self.courier_repo.get_all().all()
                headers = ["ID", "Имя", "Фамилия", "Телефон", "Зарплата", "Рейтинг", "Активен"]
                data = [
                    (c.id, c.first_name, c.last_name, c.phone_number, 
                     c.salary, c.rating, c.is_active)
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
                headers = ["ID", "Тип товара", "Получатель", "Телефон", "Адрес", "Стоимость", "Доставлено"]
                data = [
                    (d.id, d.item_type, d.recipient_name, d.recipient_phone,
                    d.recipient_address, d.item_cost, d.is_delivered)
                    for d in deliveries
                ]
                return headers, data

            
            return [], []
        
        except Exception as err:
            print(f"Ошибка получения данных таблицы: {err}")
            return [], []
    
    # --- Методы для получения списков сущностей ---
    
    def get_publishers(self):
        """
        Получает список всех активных издателей
        
        Returns:
            list: Список активных издателей
        """
        try:
            return self.publisher_repo.get_all().filter_by(is_active=True).all()
        except Exception as err:
            print(f"Ошибка получения издателей: {err}")
            return []
    
    def get_publications(self):
        """
        Получает список всех активных публикаций
        
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
    
    def get_couriers(self):
        """
        Получает список всех активных курьеров
        
        Returns:
            list: Список активных курьеров
        """
        try:
            return self.courier_repo.get_all().filter_by(is_active=True).all()
        except Exception as err:
            print(f"Ошибка получения курьеров: {err}")
            return []
    
    def get_issues(self):
        """
        Получает список всех активных выпусков
        
        Returns:
            list: Список активных выпусков
        """
        try:
            return self.show_item_repo.get_all().filter_by(on_sale=True).all()
        except Exception as err:
            print(f"Ошибка получения выпусков: {err}")
            return []
    
    # --- Методы для создания новых записей ---
    
    def create_user(self, user_data):
        """
        Создает нового пользователя
        
        Args:
            user_data (dict): Данные пользователя
            
        Returns:
            tuple: (success, user_object или error_message)
        """
        try:
            # Добавляем дату регистрации, если её нет
            if 'registration_date' not in user_data:
                user_data['registration_date'] = datetime.now()
                
            user = self.user_repo.create_user(user_data)
            return True, user
        except Exception as err:
            print(f"Ошибка создания пользователя: {err}")
            return False, str(err)
    
    def create_publisher(self, publisher_data):
        """
        Создает новое издательство
        
        Args:
            publisher_data (dict): Данные издательства
            
        Returns:
            tuple: (success, publisher_object или error_message)
        """
        try:
            # Добавляем дату начала продаж, если её нет
            if 'sales_start' not in publisher_data:
                publisher_data['sales_start'] = datetime.now()
                
            publisher = self.publisher_repo.create_publisher(publisher_data)
            return True, publisher
        except Exception as err:
            print(f"Ошибка создания издательства: {err}")
            return False, str(err)
    
    def create_publication(self, publication_data):
        """
        Создает новую публикацию
        
        Args:
            publication_data (dict): Данные публикации
            
        Returns:
            tuple: (success, publication_object или error_message)
        """
        try:
            # Добавляем дату начала продаж, если её нет
            if 'sales_start' not in publication_data:
                publication_data['sales_start'] = datetime.now()
                
            publication = self.publication_repo.create_publication(publication_data)
            return True, publication
        except Exception as err:
            print(f"Ошибка создания публикации: {err}")
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
            return True, issue
        except Exception as err:
            print(f"Ошибка создания выпуска: {err}")
            return False, str(err)
    
    def create_courier(self, courier_data):
        """
        Создает нового курьера
        
        Args:
            courier_data (dict): Данные курьера
            
        Returns:
            tuple: (success, courier_object или error_message)
        """
        try:
            courier = self.courier_repo.create_courier(courier_data)
            return True, courier
        except Exception as err:
            print(f"Ошибка создания курьера: {err}")
            return False, str(err)
    
    def create_complaint(self, complaint_data):
        """
        Создает новую жалобу
        
        Args:
            complaint_data (dict): Данные жалобы
            
        Returns:
            tuple: (success, complaint_object или error_message)
        """
        try:
            # Добавляем дату создания, если её нет
            if 'created_at' not in complaint_data:
                complaint_data['created_at'] = datetime.now()
                
            complaint = self.complaint_repo.create_complaint(complaint_data)
            return True, complaint
        except Exception as err:
            print(f"Ошибка создания жалобы: {err}")
            return False, str(err)
    
    def create_delivery(self, delivery_data):
        """
        Создает новую доставку
        
        Args:
            delivery_data (dict): Данные доставки
                
        Returns:
            tuple: (success, delivery_object или error_message)
        """
        try:
            # Проверяем наличие обязательных полей
            required_fields = ['item_id', 'item_type', 'recipient_name', 
                            'recipient_address', 'recipient_phone', 'item_cost']
            
            for field in required_fields:
                if field not in delivery_data or not delivery_data[field]:
                    return False, f"Отсутствует обязательное поле: {field}"
            
            # Получаем данные выпуска для item_id и item_type
            if 'issue_id' in delivery_data and not 'item_id' in delivery_data:
                issue_id = delivery_data['issue_id']
                issue = self.show_item_repo.find_by_id(issue_id)
                if issue:
                    delivery_data['item_id'] = issue_id
                    delivery_data['item_type'] = issue.publication_type
                else:
                    return False, f"Выпуск с ID {issue_id} не найден"
            
            # Создаем доставку через репозиторий
            delivery = self.delivery_repo.create_delivery(delivery_data)
            
            if not delivery:
                return False, "Не удалось создать доставку"
                
            return True, delivery
            
        except Exception as err:
            print(f"Ошибка создания доставки: {err}")
            return False, str(err)
    
    def get_issue_by_id(self, issue_id):
        """
        Получает выпуск по ID
        
        Args:
            issue_id (int): ID выпуска
                
        Returns:
            ShowItem: объект выпуска или None
        """
        try:
            return self.show_item_repo.find_by_id(issue_id)
        except Exception as err:
            print(f"Ошибка получения выпуска: {err}")
            return None

