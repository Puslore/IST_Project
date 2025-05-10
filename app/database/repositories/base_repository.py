from sqlalchemy.orm import Session

class BaseRepository:
    '''Базовый репозиторий, описывающий CRUD-операции моделей.'''
    def __init__(self, model_class, session: Session):
        '''
        Инициализация репозитория
        
        Arguments:
            model_class: Класс модели SQLAlchemy
            session (Session): Сессия SQLAlchemy для взаимодействия с БД
        '''
        self.model_class = model_class
        self.session = session
    
    def get_all(self):
        '''
        Получение всех записей из таблицы
        
        Returns:
            Query: SQLAlchemy Query объект со всеми записями
        '''
        return self.session.query(self.model_class)
    
    def get_by_id(self, id: int):
        '''
        Получение записи по ID с ошибкой, если не найдена
        
        Arguments:
            id (int): Идентификатор записи
        
        Returns:
            Model: Объект модели, если найден
            
        Raises:
            NoResultFound: Если запись с указанным ID не найдена
        '''
        return self.session.query(self.model_class).filter(self.model_class.id == id).one()
    
    def find_by_id(self, id: int):
        '''
        Поиск записи по ID
        
        Arguments:
            id (int): id нужной записи
        
        Returns:
            Model или None: Результат поиска записи
                - Model: если запись найдена в базе данных
                - None: если запись с указанным ID отсутствует
        '''
        return self.session.query(self.model_class).filter(self.model_class.id == id).first()
    
    def get_actives(self):
        '''
        Получение только активных записей
        
        Returns:
            Query: SQLAlchemy Query объект с активными записями
        '''
        return self.session.query(self.model_class).filter(self.model_class.is_active == True)
    
    def add(self, entity):
        '''
        Добавление новой записи
        
        Arguments:
            entity (Model): Экземпляр модели для добавления
        '''
        self.session.add(entity)
    
    def update(self, id: int, **kwargs) -> bool:
        '''
        Обновление существующей записи по ID
        
        Arguments:
            id (int): ID записи для обновления
            **kwargs: Атрибуты и их значения для обновления
        
        Returns:
            bool: Результат операции обновления
                - True: если запись найдена и успешно обновлена
                - False: если запись с указанным ID не найдена
        '''
        entity = self.find_by_id(id)
        if not entity:
            return False

        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        
        return True
    
    def soft_delete(self, id: int) -> bool:
        '''
        Мягкое удаление (установка флага is_active в False)
        
        Arguments:
            id (int): ID записи для мягкого удаления
        
        Returns:
            bool: Результат операции мягкого удаления
                - True: если запись найдена и успешно помечена как неактивная
                - False: если запись не найдена или не имеет атрибута is_active
        '''
        entity = self.find_by_id(id)
        if not entity:
            return False
            
        if hasattr(entity, 'is_active'):
            entity.is_active = False
            return True
            
        return False
    
    def permanent_delete(self, id: int) -> bool:
        '''
        Физическое удаление из базы данных
        
        Arguments:
            id (int): ID записи для удаления
        
        Returns:
            bool: Результат операции удаления
                - True: если запись найдена и успешно удалена
                - False: если запись с указанным ID не найдена
        '''
        entity = self.find_by_id(id)
        if not entity:
            return False
            
        self.session.delete(entity)
        return True
