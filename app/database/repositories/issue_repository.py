from . import BaseRepository
from app.database.models import Issue
from datetime import datetime

class IssueRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Issue, session)
    
    def create_show_item(self, data: dict) -> Issue | None:
        '''
        Создает новый выпуск издания
        
        Arguments:
            data (dict): Словарь с данными выпуска, содержащий:
                name (str): Название выпуска
                description (str): Описание выпуска
                issue_type (str): Тип издания
                publication_series_id (int): ID серии издания
                issue_number (int): Номер выпуска
                cost (float): Стоимость выпуска
                pg (int, optional): Возрастное ограничение
                is_special_edition (bool, optional): Флаг специального выпуска
        
        Returns:
            ShowItem: Созданный выпуск при успешной операции, None при ошибке
        '''
        try:
            new_show_item = Issue(
                name=data['name'],
                description=data['description'],
                issue_type=data['publication_type'],
                publication_series_id=data['publication_series_id'],
                issue_number=data['issue_number'],
                issue_date=datetime.now(),
                cost=data['cost'],
                pg=data.get('pg'),
                is_special_edition=data.get('is_special_edition', False)
            )
            
            self.add(new_show_item)
            
            if not self.commit():
                return None
            
            return new_show_item
            
        except Exception as err:
            print(f"Ошибка создания выпуска: {err}")
            return None
    
    def get_by_series(self, publication_series_id: int):
        '''
        Получает выпуски определенной серии
        
        Arguments:
            publication_series_id (int): ID серии издания
        
        Returns:
            List[ShowItem]: Список выпусков
        '''
        return self.session.query(self.model_class).filter_by(
            publication_series_id=publication_series_id
        ).order_by(self.model_class.issue_number).all()
    
    def get_latest_issues(self):
        '''
        Получает последние выпуски изданий
        
        Returns:
            List[ShowItem]: Список последних выпусков
        '''
        subquery = self.session.query(
            self.model_class.publication_series_id,
            self.model_class.issue_date.label('max_date')
        ).group_by(
            self.model_class.publication_series_id
        ).subquery()
        
        return self.session.query(self.model_class).join(
            subquery,
            (self.model_class.publication_series_id == subquery.c.publication_series_id) &
            (self.model_class.issue_date == subquery.c.max_date)
        ).all()
