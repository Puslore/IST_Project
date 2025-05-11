from . import BaseRepository
from app.database.models import Publisher

class PublisherRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Publisher, session)
    
    def create_publisher(self, data: dict) -> Publisher:
        '''
        Создает нового издателя
        
        Arguments:
            data (dict): Словарь, содержащий:
                name (str): Название издательства
                owner (str): ФИО владельца
        
        Returns:
            Publisher: Созданный издатель при успешной операции, None при ошибке
        '''
        try:
            new_publisher = Publisher(
                name=data['name'],
                owner=data['owner']
            )
            
            self.add(new_publisher)
            
            if not self.commit():
                return None
            
            return new_publisher
            
        except Exception as err:
            print(f"Ошибка создания издателя: {err}")
            return None
    
    def get_active_publishers(self):
        '''
        Получает список активных издателей
        
        Returns:
            List[Publisher]: Список активных издателей
        '''
        return self.session.query(self.model_class).filter_by(is_active=True).all()
