from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, Text, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base, Publication


class ShowItem(Base):
    '''
    Класс, определяющий конкретный выпуск печатного издания
    
    Представляет собой отдельный номер газеты или выпуск журнала в серии публикаций

    Attributes:
        id (int): Идентификатор выпуска
        issue_number (int): Номер выпуска в серии
        issue_date (datetime): Дата выпуска
        is_special_edition (bool): Флаг специального выпуска
        
        publication_type (str): Тип издания (газета, журнал)
        publication_series_id (int): Идентификатор серии издания (внешний ключ)
        publication_series (Publication): Связь с серией публикации
        
        on_sale (bool): Флаг, указывающий, доступно ли издание для продажи
        name (str): Название выпуска
        description (str): Описание выпуска
        pg (Optional[int]): Возрастное ограничение (опционально)
        
        cost (float): Стоимость данного выпуска
        discount (bool): Флаг наличия скидки на выпуск
    '''
    __tablename__ = 'show_items'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    issue_number: Mapped[int] = mapped_column(Integer, nullable=False)
    issue_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_special_edition: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    publication_type: Mapped[str] = mapped_column(Text, nullable=False)
    publication_series_id: Mapped[int] = mapped_column(
        ForeignKey("publications.id"), 
        nullable=False
    )
    publication_series: Mapped["Publication"] = relationship("Publication", back_populates="show_items")
    on_sale: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    pg: Mapped[Optional[int]] = mapped_column(Integer)

    cost: Mapped[float] = mapped_column(Float, nullable=True)
    is_discount: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    discount: Mapped[Optional[int]] = mapped_column(Integer)

    def __repr__(self) -> str:
        '''
        Возвращает строковое представление выпуска для отладки

        Returns:
            str: Строка с ID, названием издания и номером выпуска
        '''
        return f"<ShowItem(id={self.id}, name='{self.name}', issue={self.issue_number})>"
    
    def get_price(self) -> float:
        '''
        Рассчитывает итоговую цену выпуска с учетом скидки
        
        Returns:
            float: Итоговая цена после применения скидки (если есть)
        '''
        if not self.cost:
            return 0.0
            
        if self.discount:
            return self.cost * self.discount

        return self.cost

    def days_since_publication(self) -> int:
        '''
        Возвращает количество дней с момента выпуска
        
        Returns:
            int: Количество дней, прошедших с даты выпуска
        '''
        current_date = datetime.now()
        delta = current_date - self.issue_date
        return delta.days
