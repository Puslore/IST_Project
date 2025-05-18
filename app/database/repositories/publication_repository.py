from . import BaseRepository
from app.database.models import Publication

class PublicationRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Publication, session)
    
    def create_publication(self, data: dict) -> Publication | None:
        '''
        Создает новое печатное издание
        
        Arguments:
            data (dict): Словарь с данными издания, содержащий:
                name (str): Название издания
                description (str): Описание издания
                publication_type (str): Тип издания
                publisher_id (int): ID издателя
                pg (int, optional): Возрастное ограничение
        
        Returns:
            Publication: Созданное издание при успешной операции, None при ошибке
        '''
        try:
            new_publication = Publication(
                name=data['name'],
                description=data['description'],
                publication_type=data['publication_type'],
                publisher_id=data['publisher_id'],
                pg=data.get('pg')
            )
            
            self.add(new_publication)
            
            if not self.commit():
                return None
            
            return new_publication
            
        except Exception as err:
            print(f"Ошибка создания издания: {err}")
            return None
    
    def get_by_type(self, publication_type: str):
        '''
        Получает издания определенного типа
        
        Arguments:
            publication_type (str): Тип издания
        
        Returns:
            List[Publication]: Список изданий
        '''
        return self.session.query(self.model_class).filter_by(publication_type=publication_type).all()
    
    def get_by_publisher(self, publisher_id: int):
        '''
        Получает издания определенного издателя
        
        Arguments:
            publisher_id (int): ID издателя
        
        Returns:
            List[Publication]: Список изданий
        '''
        return self.session.query(self.model_class).filter_by(publisher_id=publisher_id).all()
