from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, Text, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from . import Base
from passlib.context import CryptContext

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Admin(Base):
    '''
    Класс, определяющий администратора газетного киоска

    Attributes:
        id (int): Уникальный идентификатор администратора
        first_name (str): Имя администратора
        last_name (str): Фамилия администратора
        middle_name (Optional[str]): Отчество администратора (опционально)
        phone_number (str): Контактный номер телефона в формате +XXXXXXXXXXX
        email (Optional[str]): Адрес электронной почты (опционально)
        address (str): Адрес администратора
        salary (float): Зарплата администратора
        tg_chat_id (Optional[int]): Telegram chat id администратора
        hashed_password (str): Хешированный пароль администратора
        registration_date (datetime): Дата и время регистрации администратора
        is_active (bool): Флаг, показывающий статус активности администратора
    '''
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(Text)

    phone_number: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    tg_chat_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)

    registration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        '''
        Возвращает строковое представление администратора для отладки

        Returns:
            str: Строка с ID и именем администратора
        '''
        return f"<Admin(id={self.id}, name='{self.last_name} {self.first_name}')>"

    def get_full_name(self) -> str:
        '''
        Возвращает полное имя администратора
        
        Returns:
            str: ФИО администратора
        '''
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
    def set_password(self, password: str) -> bool:
        '''
        Устанавливает хешированный пароль администратора
        
        Args:
            password (str): Пароль в открытом виде
        
        Returns:
            bool: True, если пароль успешно задан, иначе False
        '''
        self.hashed_password = pwd_context.hash(password)
        if self.hashed_password:
            return True
        return False
    
    def verify_password(self, password: str) -> bool:
        '''
        Проверяет соответствие пароля хешу
        
        Args:
            password (str): Пароль для проверки
            
        Returns:
            bool: True, если пароль верный, иначе False
        '''
        return pwd_context.verify(password, self.hashed_password)
