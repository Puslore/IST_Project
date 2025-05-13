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
    
    def commit(self) -> bool:
        '''
        Коммитит изменения в базу данных
        
        Returns:
            bool: True, если операция успешна, иначе False
        '''
        try:
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка при коммите: {e}")
            return False
    
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
    
    def add(self, entity) -> bool:
        '''
        Добавление новой записи и коммит изменений
        
        Arguments:
            entity (Model): Экземпляр модели для добавления
            
        Returns:
            bool: Результат операции добавления и коммита
                - True: если запись успешно добавлена и изменения зафиксированы
                - False: если произошла ошибка при добавлении или коммите
        '''
        try:
            self.session.add(entity)
            return self.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка при добавлении: {e}")
            return False
    
    def update(self, id: int, **kwargs: dict[str: any]) -> bool:
        '''
        Обновление существующей записи по ID и коммит изменений
        
        Arguments:
            id (int): ID записи для обновления
            **kwargs (dict[str: any]): Атрибуты и их значения для обновления
        
        Returns:
            bool: Результат операции обновления и коммита
                - True: если запись найдена, успешно обновлена и изменения зафиксированы
                - False: если запись с указанным ID не найдена или произошла ошибка при коммите
        '''
        try:
            entity = self.find_by_id(id)
            if not entity:
                return False

            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            
            return self.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка при обновлении: {e}")
            return False
    
    def soft_delete(self, id: int) -> bool:
        '''
        Мягкое удаление (установка флага is_active в False) и коммит изменений
        
        Arguments:
            id (int): ID записи для мягкого удаления
        
        Returns:
            bool: Результат операции мягкого удаления и коммита
                - True: если запись найдена, успешно помечена как неактивная и изменения зафиксированы
                - False: если запись не найдена, не имеет атрибута is_active или произошла ошибка при коммите
        '''
        try:
            entity = self.find_by_id(id)
            if not entity:
                return False
                
            if hasattr(entity, 'is_active'):
                entity.is_active = False
                return self.commit()
                
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка при мягком удалении: {e}")
            return False
    
    def permanent_delete(self, id: int) -> bool:
        '''
        Физическое удаление из базы данных и коммит изменений
        
        Arguments:
            id (int): ID записи для удаления
        
        Returns:
            bool: Результат операции удаления и коммита
                - True: если запись найдена, успешно удалена и изменения зафиксированы
                - False: если запись с указанным ID не найдена или произошла ошибка при коммите
        '''
        try:
            entity = self.find_by_id(id)
            if not entity:
                return False
                
            self.session.delete(entity)
            return self.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка при удалении: {e}")
            return False
