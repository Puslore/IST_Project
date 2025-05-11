from datetime import datetime
from typing import Optional
from sqlalchemy import Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base, Courier

class Complaint(Base):
    '''
    Класс, определяющий претензию на доставщика
    
    Attributes:
        id (int): Уникальный идентификатор претензии
        courier_id (int): Идентификатор доставщика, на которого поступила претензия
        courier (Courier): Связь с доставщиком
        created_at (datetime): Время создания претензии
        description (str): Описание претензии
    '''
    __tablename__ = 'complaints'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    courier_id: Mapped[int] = mapped_column(ForeignKey("couriers.id"), nullable=False)
    courier: Mapped["Courier"] = relationship("Courier", back_populates="complaints")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    def __repr__(self) -> str:
        '''
        Возвращает строковое представление претензии для отладки
        
        Returns:
            str: Строка с ID претензии и ID доставщика
        '''
        return f"<Complaint(id={self.id}, courier_id={self.courier_id})>"
    
    def days_since_created(self) -> int:
        '''
        Возвращает количество дней с момента создания претензии
        
        Returns:
            int: Количество дней с момента создания претензии
        '''
        current_date = datetime.now()
        delta = current_date - self.created_at
        return delta.days
