from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, Text, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models.base_model import Base


class User(Base):
    '''
    Класс, определяющий пользователя

    Attributes:
        id (int): Уникальный идентификатор пользователя
        first_name (str): Имя пользователя
        last_name (str): Фамилия пользователя
        middle_name (Optional[str]): Отчество пользователя (опционально)
        phone_number (str): Контактный номер телефона в формате +XXXXXXXXXXX
        email (Optional[str]): Адрес электронной почты (опционально)
        address (str): Физический адрес пользователя
        ad_consent (bool): Флаг согласия на получение рекламных материалов
        registration_date (datetime): Дата и время регистрации пользователя
        newspaper_subscriptions (List[int]): Список ID газет, на которые подписан пользователь
    '''
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(Text)

    phone_number: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[str] = mapped_column(Text, nullable=False)

    ad_consent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    registration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    newspaper_subscriptions: Mapped[List[int]] = mapped_column(ARRAY(Integer), default=list)

    def __repr__(self) -> str:
        '''
        Возвращает строковое представление пользователя для отладки.

        Returns:
            str: Строка с ID и именем пользователя
        '''
        return f"<User(id={self.id}, name='{self.last_name} {self.first_name}')>"

    def has_subscription(self, newspaper_id: int, newspaper_name: str = None) -> bool:
        '''
        Проверяет, подписан ли пользователь на указанную газету.

        Args:
            newspaper_id (int): ID газеты для проверки
            newspaper_name (str): название газеты для проверки

        Returns:
            bool: True, если пользователь подписан на газету, иначе False
        '''
        if newspaper_name is not None:
            return newspaper_name in self.newspaper_subscriptions
        return newspaper_id in self.newspaper_subscriptions
