from datetime import datetime
from typing import Optional, List
from sqlalchemy import Boolean, DateTime, Text, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class Delivery(Base):
    '''
    Класс, определяющий поставку товара

    Attributes:
        id (int): Идентификатор поставки
        item_id (int): Идентификатор доставляемого товара
        item_type (str): Тип доставляемого товара (газета или журнал)
        recipient_name (str): Имя получателя
        recipient_tg_chat_id (Optional[int]): Telegram chat id получателя (опционально)
        recipient_address (str): Адрес получателя
        recipient_phone (str): Телефон получателя
        item_cost (float): Стоимость товара
        is_delivered (bool): Флаг статуса доставки
        delivery_date (Optional[datetime]): Дата и время доставки
        courier_id (int): Идентефикатор курьера
        courier (Courier): Связь с курьером
    '''
    __tablename__ = 'deliveries'

    id: Mapped[int] = mapped_column(primary_key=True)

    item_id: Mapped[int] = mapped_column(ForeignKey('issues.id'), nullable=False)
    item_type: Mapped[str] = mapped_column(Text, nullable=False)

    recipient_name: Mapped[str] = mapped_column(Text, nullable=False)
    recipient_tg_chat_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.tg_chat_id'))
    recipient_address: Mapped[str] = mapped_column(Text, nullable=False)
    recipient_phone: Mapped[str] = mapped_column(Text, nullable=False)

    item_cost: Mapped[float] = mapped_column(Float, nullable=False)
    is_delivered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    delivery_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    courier_id: Mapped[int] = mapped_column(ForeignKey('couriers.id'), nullable=False)
    courier: Mapped['Courier'] = relationship('Courier', back_populates='deliveries')

    def __repr__(self) -> str:
        '''
        Возвращает строковое представление поставки для отладки

        Returns:
            str: Строка с ID и именем получателя
        '''
        return f"<Delivery(id={self.id}, recipient='{self.recipient_name}')>"

    def mark_as_delivered(self) -> None:
        '''
        Отмечает товар как доставленный и устанавливает дату доставки
        '''
        self.is_delivered = True
        self.delivery_date = datetime.now()

    def days_since_delivery(self) -> Optional[int]:
        '''
        Возвращает количество дней с момента доставки

        Returns:
            Optional[int]: Количество дней или None, если товар не доставлен
        '''
        if not self.is_delivered or not self.delivery_date:
            return None

        current_date = datetime.now()
        delta = current_date - self.delivery_date

        return delta.days
