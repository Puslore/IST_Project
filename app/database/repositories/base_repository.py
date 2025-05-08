from sqlalchemy.orm import Session

class BaseRepository:
    '''
    Базовый репозиторий, описывающий CRUD-операции моделей.
    '''
    
    def __init__(self, model_class, session: Session):
        '''
        Инициализация репозитория
        
        Args:
            model_class: Класс модели SQLAlchemy
            session: Сессия SQLAlchemy
        '''
        self.model_class = model_class
        self.session = session
    
    def get_all(self):
        '''Получение всех записей'''
        return self.session.query(self.model_class)
    
    def get_by_id(self, id: int):
        '''Получение записи по ID с ошибкой, если не найдена'''
        return self.session.query(self.model_class).filter(self.model_class.id == id).one()
    
    def find_by_id(self, id: int):
        '''Поиск записи по ID (может вернуть None)'''
        return self.session.query(self.model_class).filter(self.model_class.id == id).first()
    
    def get_actives(self):
        '''Получение только активных записей'''
        return self.session.query(self.model_class).filter(self.model_class.is_active == True)
    
    def add(self, entity, created_by_user_id: int = None):
        '''Добавление новой записи'''
        if hasattr(entity, 'created_by'):
            entity.created_by = created_by_user_id
        self.session.add(entity)
    
    def update(self, entity, updated_by_user_id: int = None):
        '''Обновление существующей записи'''
        if hasattr(entity, 'updated_by'):
            entity.updated_by = updated_by_user_id
    
    def soft_delete(self, entity, deleted_by_user_id: int = None):
        '''Мягкое удаление (установка флага is_active в False)'''
        if hasattr(entity, 'is_active'):
            entity.is_active = False
            self.update(entity, updated_by_user_id=deleted_by_user_id)
    
    def permanent_delete(self, entity):
        '''Физическое удаление из базы данных'''
        self.session.delete(entity)
