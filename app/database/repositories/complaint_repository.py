from . import BaseRepository
from app.database.models import Complaint

class ComplaintRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Complaint, session)
    
    def create_complaint(self, data: dict) -> Complaint:
        '''
        Создает новую претензию на доставщика
        
        Arguments:
            data (dict): Словарь, содержащий:
                courier_id (int): ID доставщика
                description (str): Описание претензии
        
        Returns:
            Complaint: Созданная претензия при успешной операции, None при ошибке
        '''
        try:
            new_complaint = Complaint(
                courier_id=data['courier_id'],
                description=data['description']
            )
            
            self.add(new_complaint)
            
            if not self.commit():
                return None
            
            return new_complaint
            
        except Exception as err:
            print(f"Ошибка создания претензии: {err}")
            return None
    
    def get_by_courier_id(self, courier_id: int):
        '''
        Получает список претензий для указанного доставщика
        
        Arguments:
            courier_id (int): ID доставщика
        
        Returns:
            List[Complaint]: Список претензий
        '''
        return self.session.query(self.model_class).filter_by(courier_id=courier_id).all()
