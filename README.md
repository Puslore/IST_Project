# Проект "Терминал самообслуживания для подписок на газеты и журналы

<br/>

## Тема проекта
    Информационная система для автоматизации подписки на газеты и журналы с использованием терминала самообслуживания.

<br/>

## Целевая аудитория

    Частные лица, желающие оформить подписку на печатные или электронные издания через терминал.

    Издательства, распространяющие свою продукцию через терминалы в общественных местах.

    Администраторы, управляющие ассортиментом изданий и подписками.

<br/>

## Задачи, решаемые ИС

    Регистрация и идентификация пользователей через терминал.

    Просмотр доступных газет и журналов.

    Оформление подписки на выбранные издания.

    Администрирование каталога изданий и статистики подписок.

## Аналоги на рынке

    Терминалы самообслуживания для продажи билетов, оплаты услуг (QIWI, Элекснет).

    Электронные киоски для подписки на журналы (аналогично PressReader, Readly, но с физическим терминалом).

<br/>

## Сущности

- User (Пользователь)

        id: int (PK)

        first_name, last_name: str (NOT NULL)

        middle_name: str (опционально)

        phone_number: str (NOT NULL)

        email: str (опционально)

        address: str (NOT NULL)

        tg_chat_id: int (опционально, уникальный)

        ad_consent: bool (default=False)

        registration_date: datetime (default=now)

        is_active: bool (default=True)

- Admin (Администратор)

        id: int (PK)

        first_name, last_name: str (NOT NULL)

        middle_name: str (опционально)

        phone_number: str (NOT NULL)

        email: str (опционально)

        address: str (NOT NULL)

        salary: float (NOT NULL)

        tg_chat_id: int (опционально)

        hashed_password: str (NOT NULL)

        registration_date: datetime (default=now)

        is_active: bool (default=True)

- Publisher (Издательство)

        id: int (PK)

        name, owner: str (NOT NULL)

        is_active: bool (default=True)

        sales_start: datetime (default=now)

- Publication (Издание)

        id: int (PK)

        publication_type: str (NOT NULL)

        publisher_id: int (FK → Publisher.id)

        on_sale: bool (default=True)

        sales_start: datetime (default=now)

        name, description: str (NOT NULL)

- Issue (Выпуск)

        id: int (PK)

        issue_number: int (NOT NULL)

        issue_date: datetime (NOT NULL)

        is_special_edition: bool (default=False)

        issue_type: str (NOT NULL)

        publication_id: int (FK → Publication.id)

        on_sale: bool (default=True)

        name, description: str (NOT NULL)

        pg: int (опционально)

        cost: float (опционально)

        is_discount: bool (default=False)

        discount: int (опционально)

- Courier (Курьер)

        id: int (PK)

        first_name, last_name: str (NOT NULL)

        middle_name: str (опционально)

        phone_number: str (NOT NULL)

        is_active: bool (default=True)

        salary: float (NOT NULL)

        rating: float (default=5.0)

        hire_date: datetime (default=now)

- Delivery (Доставка)

        id: int (PK)

        item_id: int (FK → Issue.id)

        item_type: str (NOT NULL)

        recipient_name: str (NOT NULL)

        recipient_tg_chat_id: int (FK → User.tg_chat_id, опционально)

        recipient_address: str (NOT NULL)

        recipient_phone: str (NOT NULL)

        item_cost: float (NOT NULL)

        is_delivered: bool (default=False)

        delivery_date: datetime (опционально)

        courier_id: int (FK → Courier.id)

- Complaint (Жалоба)

        id: int (PK)

        courier_id: int (FK → Courier.id)

        created_at: datetime (default=now)

        description: str (NOT NULL)

- user_subscriptions (Таблица связи)

        user_id: int (FK → User.id, часть PK)

        publication_id: int (FK → Publication.id, часть PK)

<br/>

## Связи между таблицами

    User ↔ Publication: многие ко многим через таблицу user_subscriptions

        Пользователь может подписаться на множество изданий

        У издания может быть множество подписчиков

    Publisher → Publication: один-ко-многим

        Издательство может выпускать множество изданий

        Издание принадлежит одному издательству

    Publication → Issue: один-ко-многим

        У издания может быть множество выпусков

        Выпуск принадлежит одному изданию

    Courier → Delivery: один-ко-многим

        Курьер может выполнять множество доставок

        Доставка выполняется одним курьером

    Courier → Complaint: один-ко-многим

        На курьера может быть подано множество жалоб

        Жалоба относится к одному курьеру

    Issue → Delivery: один-ко-многим

        Выпуск может иметь множество доставок

        Доставка относится к одному выпуску

    User → Delivery: один-ко-многим (слабая связь, только через User.tg_chat_id)

        Пользователь может получать множество доставок

        Доставка может быть связана с одним пользователем (опционально)
