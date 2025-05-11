from . import BaseRepository
from app.database.models import Delivery
from datetime import datetime

class DeliveryRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Delivery, session)
    
    def create_delivery(self, data: dict) -> Delivery:
        '''
        Создает новую запись о поставке
        
        Arguments:
            data (dict): Словарь с данными поставки, содержащий:
                item_id (int): ID товара
                item_type (str): Тип товара
                recipient_name (str): Имя получателя
                recipient_address (str): Адрес получателя
                recipient_phone (str): Телефон получателя
                item_cost (float): Стоимость товара
                recipient_tg_chat_id (int, optional): Telegram chat ID получателя
        
        Returns:
            Delivery: Созданная поставка при успешной операции, None при ошибке
        '''
        try:
            new_delivery = Delivery(
                item_id=data['item_id'],
                item_type=data['item_type'],
                recipient_name=data['recipient_name'],
                recipient_address=data['recipient_address'],
                recipient_phone=data['recipient_phone'],
                item_cost=data['item_cost'],
                recipient_tg_chat_id=data.get('recipient_tg_chat_id')
            )
            
            self.add(new_delivery)
            
            if not self.commit():
                return None
            
            return new_delivery
            
        except Exception as err:
            print(f"Ошибка создания поставки: {err}")
            return None
    
    def mark_as_delivered(self, delivery_id: int) -> bool:
        '''
        Отмечает поставку как доставленную
        
        Arguments:
            delivery_id (int): ID поставки
        
        Returns:
            bool: True при успешной операции, False при ошибке
        '''
        try:
            delivery = self.find_by_id(delivery_id)
            if not delivery:
                return False
            
            delivery.mark_as_delivered()
            
            return self.commit()
            
        except Exception as err:
            print(f"Ошибка отметки о доставке: {err}")
            return False
    
    def get_pending_deliveries(self):
        '''
        Получает список незавершенных поставок
        
        Returns:
            List[Delivery]: Список незавершенных поставок
        '''
        return self.session.query(self.model_class).filter_by(is_delivered=False).all()
