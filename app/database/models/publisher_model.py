from datetime import datetime
from typing import List
from sqlalchemy import Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class Publisher(Base):
    '''
    Класс, определяющий издательство

    Attributes:
        id (int): Уникальный идентификатор издательства
        name (str): Название издательства
        owner (str): ФИО владельца издательства
        is_active (bool): Флаг, показывающий статус активности издательства
        publications (List[Publication]): Список печатных изданий, выпускаемых издательством
        sales_start (datetime): Дата начала продаж издательства
    '''
    __tablename__ = 'publishers'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    publications: Mapped[List["Publication"]] = relationship("Publication", back_populates="publisher")
    sales_start: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self) -> str:
        '''
        Возвращает строковое представление издательства для отладки

        Returns:
            str: Строка с ID и названием издательства
        '''
        return f"<Publisher(id={self.id}, name='{self.name}')>"

    def get_active_publications(self):
        '''
        Возвращает список активных публикаций издательства
        
        Returns:
            List[Publication]: Список активных публикаций
        '''
        return [pub for pub in self.publications if pub.on_sale]

