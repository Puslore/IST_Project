from app.database.session import get_session
from app.database.repositories import UserRepository, IssueRepository, PublicationRepository


class Controller:
    def __init__(self):
        self.session = None
        self.user_repo = None
        self.publication_repo = None
        self.show_item_repo = None
        self._init_repositories()
    
    def _init_repositories(self):
        """Инициализация репозиториев с новой сессией"""
        with get_session() as session:
            self.session = session
            self.user_repo = UserRepository(session)
            self.publication_repo = PublicationRepository(session)
            self.show_item_repo = IssueRepository(session)
    
    def create_user(self, user_data: dict):
        """
        Создает нового пользователя
        
        Args:
            user_data (dict): Данные пользователя
            
        Returns:
            tuple: (success, user или error_message)
        """
        try:
            new_user = self.user_repo.registration(user_data)
            if not new_user:
                print('Ошибка регистрации пользователя в контроллере окна')
                return False, "Ошибка регистрации пользователя"
            return True, new_user

        except ValueError as err:
            print(f'Error in user window controller - {err}')
            return False, str(err)

        except Exception as err:
            print(f'Error in user window controller - {err}')
            return False, "Неизвестная ошибка при регистрации"
    
    def get_user_by_id(self, user_id: int):
        """
        Получает пользователя по ID
        
        Args:
            user_id (int): ID пользователя
            
        Returns:
            User: Объект пользователя или None
        """
        try:
            return self.user_repo.find_by_id(user_id)
        except Exception as err:
            print(f'Ошибка получения пользователя: {err}')
            return None
    
    def get_user_by_phone(self, phone_number: str):
        """
        Получает пользователя по номеру телефона
        
        Args:
            phone_number (str): Номер телефона
            
        Returns:
            User: Объект пользователя или None
        """
        try:
            return self.user_repo.find_by_phone(phone_number)
        except Exception as err:
            print(f'Ошибка получения пользователя по телефону: {err}')
            return None
    
    def update_user_profile(self, user_id: int, phone: str, email: str, address: str):
        """
        Обновляет профиль пользователя
        
        Args:
            user_id (int): ID пользователя
            phone (str): Номер телефона
            email (str): Email
            address (str): Адрес
            
        Returns:
            bool: True если обновление прошло успешно, иначе False
        """
        try:
            return self.user_repo.update(user_id, phone_number=phone, email=email, address=address)
        except Exception as err:
            print(f'Ошибка обновления профиля: {err}')
            return False
    
    def get_user_subscriptions(self, user_id: int):
        """
        Получает список подписок пользователя
        
        Args:
            user_id (int): ID пользователя
            
        Returns:
            list: Список подписок
        """
        try:
            user = self.user_repo.find_by_id(user_id)
            if not user:
                return []
            return user.subscribed_publications
        except Exception as err:
            print(f'Ошибка получения подписок: {err}')
            return []
    
    def get_all_publications(self):
        """
        Получает список всех доступных изданий
        
        Returns:
            list: Список изданий
        """
        try:
            return self.publication_repo.get_all().filter_by(on_sale=True).all()
        except Exception as err:
            print(f'Ошибка получения изданий: {err}')
            return []
    
    def get_publications_by_type(self, pub_type: str):
        """
        Получает издания определенного типа
        
        Args:
            pub_type (str): Тип издания
            
        Returns:
            list: Список изданий
        """
        try:
            return self.publication_repo.get_by_type(pub_type)
        except Exception as err:
            print(f'Ошибка получения изданий по типу: {err}')
            return []
    
    def subscribe_user_to_publication(self, user_id: int, publication_id: int):
        """
        Подписывает пользователя на издание
        
        Args:
            user_id (int): ID пользователя
            publication_id (int): ID издания
            
        Returns:
            bool: True если подписка оформлена успешно, иначе False
        """
        try:
            user = self.user_repo.find_by_id(user_id)
            publication = self.publication_repo.find_by_id(publication_id)
            
            if not user or not publication:
                return False
            
            # Проверяем, есть ли уже такая подписка
            if user.has_subscription(publication_id=publication_id):
                return False
            
            # Добавляем публикацию в подписки пользователя
            user.subscribed_publications.append(publication)
            return self.user_repo.commit()
        except Exception as err:
            print(f'Ошибка оформления подписки: {err}')
            return False
    
    def unsubscribe_user_from_publication(self, user_id: int, publication_id: int):
        """
        Отменяет подписку пользователя на издание
        
        Args:
            user_id (int): ID пользователя
            publication_id (int): ID издания
            
        Returns:
            bool: True если отмена прошла успешно, иначе False
        """
        try:
            user = self.user_repo.find_by_id(user_id)
            publication = self.publication_repo.find_by_id(publication_id)
            
            if not user or not publication:
                return False
                
            # Удаляем публикацию из подписок пользователя
            user.subscribed_publications.remove(publication)
            return self.user_repo.commit()
        except Exception as err:
            print(f'Ошибка отмены подписки: {err}')
            return False
