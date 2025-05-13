from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, Text, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base

class Courier(Base):
    '''
    Класс, определяющий доставщика печатных изданий
    
    Attributes:
        id (int): Уникальный идентификатор доставщика
        first_name (str): Имя доставщика
        last_name (str): Фамилия доставщика
        middle_name (Optional[str]): Отчество доставщика (опционально)
        is_active (bool): Флаг, показывающий статус активности доставщика
        phone_number (str): Телефон доставщика
        salary (float): Зарплата доставщика
        rating (float): Рейтинг доставщика
        hire_date (datetime): Дата устройства на работу
        complaints (List["Complaint"]): Список претензий на доставщика
    '''
    __tablename__ = 'couriers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(Text)
    phone_number: Mapped[str] = mapped_column(Text, nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=5.0)
    hire_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    
    complaints: Mapped[List["Complaint"]] = relationship("Complaint", back_populates="courier")
    
    def __repr__(self) -> str:
        '''
        Возвращает строковое представление доставщика для отладки
        
        Returns:
            str: Строка с ID и именем доставщика
        '''
        return f"<Courier(id={self.id}, name='{self.last_name} {self.first_name}')>"
    
    def get_full_name(self) -> str:
        '''
        Возвращает полное имя доставщика
        
        Returns:
            str: Полное имя доставщика в формате "Фамилия Имя Отчество"
        '''
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
    def update_rating(self, new_rating: float) -> None:
        '''
        Обновляет рейтинг доставщика
        
        Args:
            new_rating (float): Новое значение рейтинга
        '''
        self.rating = new_rating
