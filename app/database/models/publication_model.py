from datetime import datetime
from typing import List
from sqlalchemy import Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user_subscription_model import user_subscriptions
from . import Base


class Publication(Base):
    '''
    Класс, определяющий печатное издание

    Attributes:
        id (int): Идентификатор печатного издания
        publication_type (str): Тип издания (газета, журнал)
        publisher_id (int): Идентификатор издателя (внешний ключ)
        publisher (Publisher): Издатель данного печатного издания
        on_sale (bool): Флаг, указывающий, доступно ли издание для продажи
        sales_start (datetime): Дата начала продаж
        name (str): Название издания
        description (str): Описание издания
        
        show_items (List["Issue"]): Связанные выпуски данного издания
        subscribers (List[User]): Пользователи, подписанные на издание
    '''
    __tablename__ = 'publications'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    publication_type: Mapped[str] = mapped_column(Text, nullable=False)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"), nullable=False)
    publisher: Mapped["Publisher"] = relationship("Publisher", back_populates="publications")
    on_sale: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sales_start: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    # pg: Mapped[Optional[int]] = mapped_column(Integer)
    
    issues: Mapped[List["Issue"]] = relationship("Issue", back_populates="publication")

    subscribers: Mapped[List["User"]] = relationship(
        "User",
        secondary=user_subscriptions,
        back_populates="subscribed_publications"
    )

    def __repr__(self) -> str:
        '''
        Возвращает строковое представление печатного издания для отладки

        Returns:
            str: Строка с ID и названием издания
        '''
        return f"<Publication(id={self.id}, name='{self.name}')>"
    
    def is_subscriber(self, user) -> bool:
        '''
        Проверяет, является ли пользователь подписчиком издания
        
        Args:
            user (User): Пользователь для проверки
            
        Returns:
            bool: True, если пользователь подписан, иначе False
        '''
        return user in self.subscribers

    def get_latest_issue(self):
        '''
        Возвращает последний выпуск издания
        
        Returns:
            Issue: Последний выпуск или None, если выпусков нет
        '''
        if not self.issues:
            return None
        return max(self.issues, key=lambda issue: issue.issue_date)
