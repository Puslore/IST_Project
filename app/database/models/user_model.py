from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base


class User(Base):
    '''
    Класс, определяющий пользователя

    Attributes:
        id (int): Идентификатор пользователя
        first_name (str): Имя пользователя
        last_name (str): Фамилия пользователя
        middle_name (Optional[str]): Отчество пользователя (опционально)
        phone_number (str): Контактный номер телефона в формате +XXXXXXXXXXX
        email (Optional[str]): Адрес электронной почты (опционально)
        address (str): Физический адрес пользователя
        tg_chat_id (int): Telegram chat id
        ad_consent (bool): Флаг согласия на получение рекламных материалов
        registration_date (datetime): Дата и время регистрации пользователя
        is_active (bool): Флаг, показывающий статус активности пользователя
        subscribed_publications (List[Publication]): Список изданий, на которые подписан пользователь
    '''
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(Text)

    phone_number: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    tg_chat_id: Mapped[Optional[int]] = mapped_column(Integer)

    ad_consent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    registration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    subscribed_publications: Mapped[List["Publication"]] = relationship(
        "Publication",
        secondary="user_subscriptions",
        back_populates="subscribers"
    )

    def __repr__(self) -> str:
        '''
        Возвращает строковое представление пользователя для отладки

        Returns:
            str: Строка с ID и именем пользователя
        '''
        return f"<User(id={self.id}, name='{self.last_name} {self.first_name}')>"

    def has_subscription(self, publication_id: int = None, publication_name: str = None) -> bool:
        '''
        Проверяет, подписан ли пользователь на указанное издание

        Args:
            publication_id (int, optional): ID издания для проверки
            publication_name (str, optional): Название издания для проверки

        Returns:
            bool: True, если пользователь подписан на издание, иначе False
            
        Примечание:
            Необходимо указать хотя бы один из параметров: publication_id или publication_name
        '''
        if publication_id is not None:
            return any(pub.id == publication_id for pub in self.subscribed_publications)
            
        if publication_name is not None:
            return any(pub.name == publication_name for pub in self.subscribed_publications)
            
        return False
    
    def get_full_name(self) -> str:
        '''
        Возвращает полное имя пользователя
        
        Returns:
            str: Полное имя пользователя в формате "Фамилия Имя Отчество"
        '''
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
