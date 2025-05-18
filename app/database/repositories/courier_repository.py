from . import BaseRepository
from app.database.models import Courier

class CourierRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Courier, session)
    
    def create_courier(self, data: dict) -> Courier | None:
        '''
        Создает нового доставщика в системе
        
        Arguments:
            data (dict): Словарь с данными доставщика, содержащий:
                first_name (str): Имя доставщика
                last_name (str): Фамилия доставщика
                salary (float): Зарплата доставщика
                middle_name (str, optional): Отчество доставщика
                phone_number (str): Телефон доставщика
        
        Returns:
            Courier: Созданный доставщик при успешной регистрации, None при ошибке
        '''
        try:
            new_courier = Courier(
                first_name=data['first_name'],
                last_name=data['last_name'],
                middle_name=data.get('middle_name'),
                salary=data['salary'],
                phone_number=data['phone_number']
            )
            
            self.add(new_courier)
            
            if not self.commit():
                return None
            
            return new_courier
            
        except Exception as err:
            print(f"Ошибка создания доставщика: {err}")
            return None
    
    def get_by_rating(self, min_rating: float | None = None,
                                  max_rating: float | None = None):
        '''
        Получает доставщиков с указанным рейтингом
        
        Arguments:
            min_rating (float, optional): Минимальный рейтинг
            max_rating (float, optional): Максимальный рейтинг
        
        Returns:
            Query: SQLAlchemy Query объект с доставщиками
        '''
        query = self.session.query(self.model_class)
        
        if min_rating is not None:
            query = query.filter(self.model_class.rating >= min_rating)
        
        if max_rating is not None:
            query = query.filter(self.model_class.rating <= max_rating)
            
        return query
    
    def get_active_couriers(self):
        '''
        Получает список активных доставщиков
        
        Returns:
            List[Courier]: Список активных доставщиков
        '''
        return self.session.query(self.model_class).filter_by(is_active=True).all()
