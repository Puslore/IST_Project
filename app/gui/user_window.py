from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QCheckBox,
                             QPushButton, QFormLayout, QStackedWidget, QDialog,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QComboBox, QGroupBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from app.controllers.user_window_controller import Controller
from app.controllers.bot_controller import BotController
from app.bot.generate_auth_code import generate_auth_code
import asyncio

class Main_Window(QMainWindow):
    def __init__(self, window_controller=Controller(), bot_controller = BotController()):
        """
        Инициализация окна регистрации/входа.
        
        Args:
            controller: Контроллер для работы с БД
        """
        # Вызов конструктора родительского класса QMainWindow
        super().__init__()
        
        # Ссылки на контроллеры
        self.window_controller = window_controller
        self.bot_controller = bot_controller
        
        # Настройка основного окна
        self.setWindowTitle("Терминал газетного киоска")
        self.setFixedSize(500, 800)
        self.setStyleSheet("background-color: #f8f3e6;")  # Бежевый фон
        
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной макет
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        
        # Заголовок
        title_label = QLabel("ТЕРМИНАЛ ГАЗЕТНОГО КИОСКА")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(18)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Кнопки верхней панели
        button_layout = QHBoxLayout()
        
        self.register_button = QPushButton("РЕГИСТРАЦИЯ")
        self.register_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 15px; font-weight: bold; border-radius: 5px;"
        )
        
        self.login_button = QPushButton("ВОЙТИ")
        self.login_button.setStyleSheet(
            "background-color: white; color: black; padding: 15px; border: 1px solid black; border-radius: 5px;"
        )
        
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.login_button)
        main_layout.addLayout(button_layout)
        
        # Создаем стек виджетов для переключения между формами
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Создаем формы регистрации и входа
        self.register_form_widget = self.create_register_form()
        self.login_form_widget = self.create_login_form()
        
        # Добавляем формы в стек
        self.stacked_widget.addWidget(self.register_form_widget)
        self.stacked_widget.addWidget(self.login_form_widget)
        
        # По умолчанию показываем форму регистрации
        self.stacked_widget.setCurrentIndex(0)
        
        # Установка макета
        main_layout.setContentsMargins(30, 20, 30, 30)
        
        # Подключение сигналов
        self.register_button.clicked.connect(self.show_register_form)
        self.login_button.clicked.connect(self.show_login_form)
    
    def create_register_form(self):
        """Создает виджет с формой регистрации"""
        form_widget = QWidget()
        layout = QVBoxLayout(form_widget)
        
        # Форма ввода
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(25)
        
        # Стили для полей ввода и меток
        label_style = "font-size: 14px; font-weight: bold;"
        input_style = "padding: 12px; border: 1px solid black; border-radius: 5px; background-color: #f8f3e6;"
        
        # Поля формы с сохранением ссылок
        self.register_fields = {}
        
        fields = [
            ("first_name", "ИМЯ", ""),
            ("last_name", "ФАМИЛИЯ", ""),
            ("middle_name", "ОТЧЕСТВО (ПРИ НАЛИЧИИ)", ""),
            ("phone_number", "НОМЕР ТЕЛЕФОНА", ""),
            ("address", "АДРЕС", ""),
            ("email", "ПОЧТА (ОПЦИОНАЛЬНО)", "")
        ]
        
        for field_name, label_text, placeholder in fields:
            label = QLabel(label_text)
            label.setStyleSheet(label_style)
            
            input_field = QLineEdit()
            input_field.setStyleSheet(input_style)
            input_field.setPlaceholderText(placeholder)
            input_field.setMinimumHeight(50)
            
            # Сохраняем ссылку на поле ввода
            self.register_fields[field_name] = input_field
            
            form_layout.addRow(label, input_field)
        
        layout.addLayout(form_layout)
        
        # Чекбокс согласия
        self.agree_checkbox = QCheckBox("Согласен на рассылку рекламы")
        self.agree_checkbox.setStyleSheet("font-size: 14px; margin-top: 10px;")
        self.agree_checkbox.setChecked(False)
        layout.addWidget(self.agree_checkbox)
        
        # Кнопка регистрации
        register_button_bottom = QPushButton("ЗАРЕГИСТРИРОВАТЬСЯ")
        register_button_bottom.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 15px; font-weight: bold; " 
            "border-radius: 5px; font-size: 14px; margin-top: 20px;"
        )
        register_button_bottom.setMinimumHeight(60)
        register_button_bottom.clicked.connect(self.register_user)
        layout.addWidget(register_button_bottom)
        
        return form_widget
    
    def create_login_form(self):
        """Создает виджет с формой входа"""
        if hasattr(self, 'current_user'):
            self.current_user = None
        login_widget = QWidget()
        layout = QVBoxLayout(login_widget)
        
        # Стили
        label_style = "font-size: 14px; font-weight: bold;"
        input_style = "padding: 12px; border: 1px solid black; border-radius: 5px; background-color: #f8f3e6;"
        button_style = "padding: 15px; font-weight: bold; border-radius: 5px; font-size: 14px; margin-top: 20px;"
        
        # Поле для номера телефона
        phone_label = QLabel("НОМЕР ТЕЛЕФОНА")
        phone_label.setStyleSheet(label_style)
        
        self.login_phone = QLineEdit()
        self.login_phone.setStyleSheet(input_style)
        self.login_phone.setMinimumHeight(50)
        
        layout.addWidget(phone_label)
        layout.addWidget(self.login_phone)
        layout.addSpacing(30)
        
        # Кнопки входа
        sms_button = QPushButton("ВОЙТИ ПО SMS")
        sms_button.setStyleSheet(
            f"background-color: #1e1e1e; color: white; {button_style}"
        )
        sms_button.setMinimumHeight(60)
        sms_button.clicked.connect(self.login_via_sms)
        
        tg_button = QPushButton("ВОЙТИ С ПОМОЩЬЮ КОДА ИЗ TG-БОТА")
        tg_button.setStyleSheet(
            f"background-color: #1e1e1e; color: white; {button_style}"
        )
        tg_button.setMinimumHeight(60)
        # phone = self.login_phone.text()
        # user = self.window_controller.get_user_by_phone(phone)
        # if user is not None:
            # self.waiting_auth_code_user = user
        # print({user.__repr__})
        tg_button.clicked.connect(self.login_via_telegram)
        
        layout.addWidget(sms_button)
        layout.addSpacing(15)
        layout.addWidget(tg_button)
        
        # Добавляем автоматическое растяжение пространства
        layout.addStretch()
        
        return login_widget
    
    def show_register_form(self):
        """Переключает на форму регистрации"""
        # Меняем стили кнопок
        self.register_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 15px; font-weight: bold; border-radius: 5px;"
        )
        self.login_button.setStyleSheet(
            "background-color: white; color: black; padding: 15px; border: 1px solid black; border-radius: 5px;"
        )
        
        # Показываем форму регистрации
        self.stacked_widget.setCurrentIndex(0)
    
    def show_login_form(self):
        """Переключает на форму входа"""
        # Меняем стили кнопок
        self.register_button.setStyleSheet(
            "background-color: white; color: black; padding: 15px; border: 1px solid black; border-radius: 5px;"
        )
        self.login_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 15px; font-weight: bold; border-radius: 5px;"
        )
        
        # Показываем форму входа
        self.stacked_widget.setCurrentIndex(1)
    
    def register_user(self):
        """Метод для обработки регистрации пользователя"""
        if not self.window_controller:
            print("Контроллер не инициализирован")
            return
        
        # Сбор данных из формы
        user_data = {
            "first_name": self.register_fields["first_name"].text(),
            "last_name": self.register_fields["last_name"].text(),
            "middle_name": self.register_fields["middle_name"].text() or None,
            "phone_number": self.register_fields["phone_number"].text(),
            "address": self.register_fields["address"].text(),
            "email": self.register_fields["email"].text() or None,
            "ad_consent": self.agree_checkbox.isChecked()
        }
        
        # Вызов метода контроллера для создания пользователя
        result = self.window_controller.create_user(user_data)
        
        # Обработка результата (можно добавить диалоговое окно с сообщением)
        if result[0] == True and result is not None:
            print("Пользователь успешно зарегистрирован")
            self.clear_form()
            self.show_personal_cabinet(result[1])
        
        else:
            print("Ошибка при регистрации пользователя")
            
    
    def clear_form(self):
        """Очистка полей формы после успешной регистрации"""
        for field in self.register_fields.values():
            field.clear()
    
# TODO
    def login_via_sms(self):
        """Вход по SMS (для демо просто выводим сообщение)"""
        phone = self.login_phone.text()
        print(f'{phone=}')
        print(f"Вход по SMS для номера: {phone}")
        # Здесь НЕ будет интеграции с реальной системой SMS в будущем
        user = self.window_controller.get_user_by_phone(phone)
        
        if user is not None:
            self.show_personal_cabinet(user)
        
        else:
            self.show_login_form()
    
# TODO
    def login_via_telegram(self):
        """Вход с помощью кода из Telegram"""
        phone = self.login_phone.text()
        user = self.window_controller.get_user_by_phone(phone)
        if user is not None:
            self.waiting_auth_code_user = user
            print({user.__repr__})
        print(f"Запрошен вход через Telegram для номера: {phone}")
        self.show_code_waiting_dialog()
    
    def show_code_waiting_dialog(self):
        """Показывает диалог ожидания кода из Telegram"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Ожидание кода")
        dialog.setFixedSize(300, 200)
        
        layout = QVBoxLayout(dialog)
        
        label = QLabel("Пожалуйста, введите код из Telegram:")
        layout.addWidget(label)
        
        self.auth_code_input = QLineEdit()
        self.auth_code_input.setPlaceholderText("Код из Telegram")
        layout.addWidget(self.auth_code_input)
        
        user = self.waiting_auth_code_user
        self.tg_auth_code = self.bot_controller.generate_auth_code_for_user(user.id)
        user_tg_chat_id = user.tg_chat_id
        asyncio.create_task(self.bot_controller.send_login_code(self.tg_auth_code, user_tg_chat_id))
        
        confirm_button = QPushButton("Подтвердить")
        confirm_button.clicked.connect(lambda: self.confirm_telegram_code(dialog))
        layout.addWidget(confirm_button)
        
        dialog.exec()
    
    def confirm_telegram_code(self, dialog):
        """Обработка кода из Telegram"""
        user = self.waiting_auth_code_user
        if self.auth_code_input.text() == str(self.tg_auth_code):
            
            # self.show_personal_cabinet(user)
            self.login_successful(user_id=user.id)
        
        else:
            # print(f'Ошибка при авторизации пользователя:\n{user_tg_chat_id=}\n{tg_auth_code=}\n{check_auth=}')
            print('Ошибка при авторизации пользователя')
            self.current_user = user
            self.auth_code_input.clear()
            self.bot_controller.remove_verify_code(self.tg_auth_code)
            
            self.show_code_waiting_dialog()
            
        dialog.accept()
    
    # def login_successful(self):
    #     """Обработка успешного входа"""
    #     self.show_personal_cabinet()
    
    def create_personal_cabinet(self, user):
        """Создает виджет с личным кабинетом пользователя"""
        # self.current_user
        cabinet_widget = QWidget()
        layout = QVBoxLayout(cabinet_widget)

        # Верхняя панель с именем пользователя и кнопкой выхода
        top_panel = QHBoxLayout()
        
        # Имя пользователя
        user_label = QLabel(f"Здравствуйте, {user.get_full_name()}!")
        user_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_panel.addWidget(user_label, 1)

        # Кнопка выхода
        logout_button = QPushButton("ВЫХОД")
        logout_button.setStyleSheet(
            "background-color: white; color: black; padding: 10px; "
            "border: 1px solid black; border-radius: 5px; max-width: 100px;"
        )
        logout_button.clicked.connect(self.logout)
        top_panel.addWidget(logout_button)
        layout.addLayout(top_panel)
        layout.addSpacing(20)

        # Секция подписок
        subscriptions_label = QLabel("МОИ ПОДПИСКИ")
        subscriptions_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(subscriptions_label)

        # Список подписок
        if hasattr(user, 'subscribed_publications') and user.subscribed_publications:
            # Создаем таблицу с подписками
            subscriptions_table = QTableWidget()
            subscriptions_table.setColumnCount(3)
            subscriptions_table.setHorizontalHeaderLabels(["Название", "Тип", "Статус"])
            subscriptions_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            subscriptions_table.setStyleSheet("background-color: white; border: 1px solid #ddd;")
            
            # Заполняем таблицу данными о подписках
            subscriptions_table.setRowCount(len(user.subscribed_publications))
            for row, pub in enumerate(user.subscribed_publications):
                subscriptions_table.setItem(row, 0, QTableWidgetItem(pub.name))
                subscriptions_table.setItem(row, 1, QTableWidgetItem(pub.publication_type))
                subscriptions_table.setItem(row, 2, QTableWidgetItem("Активна" if pub.on_sale else "Не активна"))
                
                # Добавляем кнопку для просмотра последнего выпуска
                if hasattr(pub, 'issues') and pub.issues:
                    latest_issue = None
                    try:
                        latest_issue = pub.get_latest_issue()
                    except Exception:
                        pass
                        
                    if latest_issue:
                        issue_button = QPushButton("Последний выпуск")
                        issue_button.setStyleSheet("background-color: #1e1e1e; color: white; padding: 5px;")
                        issue_button.clicked.connect(lambda checked, i=latest_issue: self.show_issue_details(i))
                        subscriptions_table.setCellWidget(row, 3, issue_button)
            
            self.subscriptions_list = subscriptions_table

        else:
            self.subscriptions_list = QLabel("У вас пока нет активных подписок")
            self.subscriptions_list.setStyleSheet(
                "background-color: white; padding: 20px; border: 1px solid #ddd; "
                "min-height: 200px; border-radius: 5px;"
            )
        
        layout.addWidget(self.subscriptions_list)


        # Добавляем дополнительные секции
        
        # Секция профиля
        profile_section = QGroupBox("ПРОФИЛЬ")
        profile_section.setStyleSheet("margin-top: 20px;")
        profile_layout = QVBoxLayout(profile_section)
        
        # Добавляем информацию о профиле
        profile_info = QLabel(
            f"<b>Телефон:</b> {user.phone_number}<br>"
            f"<b>Email:</b> {user.email or 'Не указан'}<br>"
            f"<b>Адрес:</b> {user.address}"
        )
        profile_info.setStyleSheet("background-color: white; padding: 15px; border-radius: 5px;")
        profile_layout.addWidget(profile_info)
        
        # Кнопка редактирования профиля
        edit_profile_button = QPushButton("РЕДАКТИРОВАТЬ ПРОФИЛЬ")
        edit_profile_button.setStyleSheet(
            "background-color: white; color: black; padding: 10px; "
            "border: 1px solid black; border-radius: 5px; margin-top: 10px;"
        )
        edit_profile_button.clicked.connect(self.edit_profile)
        profile_layout.addWidget(edit_profile_button)
        
        layout.addWidget(profile_section)

        # Кнопки основных действий
        subscribe_button = QPushButton("ОФОРМИТЬ ПОДПИСКУ")
        subscribe_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 15px; font-weight: bold; "
            "border-radius: 5px; font-size: 14px; margin-top: 20px;"
        )
        subscribe_button.setMinimumHeight(60)
        subscribe_button.clicked.connect(self.show_subscription_dialog)
        layout.addWidget(subscribe_button)

        # Кнопка подключения Telegram-бота
        connect_telegram_button = QPushButton("ПОДКЛЮЧИТЬ TELEGRAM-БОТА ДЛЯ АВТОРИЗАЦИИ")
        connect_telegram_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 15px; font-weight: bold; "
            "border-radius: 5px; font-size: 14px; margin-top: 20px;"
        )
        connect_telegram_button.setMinimumHeight(60)
        connect_telegram_button.clicked.connect(self.show_telegram_connect_dialog)
        layout.addWidget(connect_telegram_button)

        # Добавляем автоматическое растяжение пространства
        layout.addStretch()
        
        return cabinet_widget
    
    def show_issue_details(self, issue):
        """Показывает детальную информацию о выпуске"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{issue.name} (№{issue.issue_number})")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(dialog)
        
        # Информация о выпуске
        title = QLabel(issue.name)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Основные данные
        details_layout = QFormLayout()
        details_layout.addRow("Тип издания:", QLabel(issue.publication_type))
        details_layout.addRow("Номер выпуска:", QLabel(str(issue.issue_number)))
        details_layout.addRow("Дата выпуска:", QLabel(issue.issue_date.strftime("%d.%m.%Y")))
        
        # Добавляем стоимость с учетом скидки
        if hasattr(issue, "is_discount") and issue.is_discount and issue.discount:
            original_price = QLabel(f"{issue.cost} руб.")
            original_price.setStyleSheet("text-decoration: line-through;")
            
            discount_price = issue.cost - (issue.cost * issue.discount / 100)
            discounted_price = QLabel(f"{discount_price:.2f} руб. ({issue.discount}% скидка)")
            discounted_price.setStyleSheet("color: red; font-weight: bold;")
            
            price_layout = QHBoxLayout()
            price_layout.addWidget(original_price)
            price_layout.addWidget(discounted_price)
            
            details_layout.addRow("Стоимость:", price_layout)
        else:
            details_layout.addRow("Стоимость:", QLabel(f"{issue.cost} руб."))
        
        layout.addLayout(details_layout)
        
        # Описание
        description_label = QLabel("Описание:")
        description_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(description_label)
        
        description = QLabel(issue.description)
        description.setWordWrap(True)
        description.setStyleSheet("background-color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(description)
        
        # Кнопка закрытия
        close_button = QPushButton("ЗАКРЫТЬ")
        close_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 10px; "
            "border-radius: 5px; margin-top: 20px;"
        )
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        
        dialog.exec()


# TODO
    def edit_profile(self):
        """Открывает окно редактирования профиля"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Редактирование профиля")
        dialog.setFixedSize(400, 400)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Стили для полей
        input_style = "padding: 12px; border: 1px solid black; border-radius: 5px; background-color: #f8f3e6;"
        
        # Создаем поля для редактирования
        phone_field = QLineEdit()
        phone_field.setStyleSheet(input_style)
        phone_field.setText(self.current_user.phone_number)
        
        email_field = QLineEdit()
        email_field.setStyleSheet(input_style)
        email_field.setText(self.current_user.email or "")
        
        address_field = QLineEdit()
        address_field.setStyleSheet(input_style)
        address_field.setText(self.current_user.address)
        
        # Добавляем поля в форму
        form_layout.addRow("Телефон:", phone_field)
        form_layout.addRow("Email:", email_field)
        form_layout.addRow("Адрес:", address_field)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("СОХРАНИТЬ")
        save_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 12px; "
            "font-weight: bold; border-radius: 5px;"
        )
        save_button.clicked.connect(lambda: self.save_profile(
            dialog, phone_field.text(), email_field.text(), address_field.text()
        ))
        
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 12px; "
            "border: 1px solid black; border-radius: 5px;"
        )
        cancel_button.clicked.connect(dialog.reject)
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout)
        
        dialog.exec()

    def save_profile(self, dialog, phone, email, address):
        """Сохраняет изменения в профиле пользователя"""
        # Обновляем данные пользователя через контроллер
        success = self.window_controller.update_user_profile(
            self.current_user.id, phone, email, address
        )
        
        if success:
            dialog.accept()
            # Обновляем пользователя и перерисовываем личный кабинет
            self.current_user = self.window_controller.get_user_by_id(self.current_user.id)
            self.refresh_personal_cabinet()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить профиль")

    def show_subscription_dialog(self):
        """Показывает диалог для оформления подписки"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Доступные издания")
        dialog.setFixedSize(600, 500)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(dialog)
        
        # Заголовок
        title = QLabel("КАТАЛОГ ИЗДАНИЙ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Фильтры
        filter_layout = QHBoxLayout()
        
        # Фильтр по жанру
        genre_label = QLabel("Жанр:")
        genre_combo = QComboBox()
        genre_combo.addItems(["Все жанры", "Новости", "Спорт", "Наука", "Мода", "Развлечения"])
        genre_combo.setStyleSheet("padding: 8px; background-color: white; border: 1px solid #ddd;")
        
        # Фильтр по типу печати
        print_label = QLabel("Тип печати:")
        print_combo = QComboBox()
        print_combo.addItems(["Все типы", "Газета", "Журнал", "Бюллетень"])
        print_combo.setStyleSheet("padding: 8px; background-color: white; border: 1px solid #ddd;")
        
        filter_layout.addWidget(genre_label)
        filter_layout.addWidget(genre_combo)
        filter_layout.addSpacing(15)
        filter_layout.addWidget(print_label)
        filter_layout.addWidget(print_combo)
        
        layout.addLayout(filter_layout)
        layout.addSpacing(15)
        
        # Список доступных изданий        
        publications_table = QTableWidget()
        publications_table.setColumnCount(2)
        publications_table.setHorizontalHeaderLabels(["Название", "Тип"])
        publications_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        publications_table.setStyleSheet("background-color: white; border: 1px solid #ddd;")
        publications_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Получаем список публикаций
        publications = self.window_controller.get_all_publications()
        self.publications_data = publications  # Сохраняем данные о публикациях
        
        publications_table.setRowCount(len(publications))
        
        for row, publication in enumerate(publications):
            publications_table.setItem(row, 0, QTableWidgetItem(publication.name))
            publications_table.setItem(row, 1, QTableWidgetItem(publication.publication_type))
            # publications_table.setItem(row, 2, QTableWidgetItem(str(publication.cost)))
        
        layout.addWidget(publications_table)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        subscribe_button = QPushButton("ПОДПИСАТЬСЯ")
        subscribe_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 12px; "
            "font-weight: bold; border-radius: 5px;"
        )
        # Подключаем обработчик к кнопке подписки
        subscribe_button.clicked.connect(lambda: self.handle_subscription(dialog, publications_table))
        
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 12px; "
            "border: 1px solid black; border-radius: 5px;"
        )
        cancel_button.clicked.connect(dialog.reject)
        
        buttons_layout.addWidget(subscribe_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        dialog.exec()
    
    def handle_subscription(self, dialog, publications_table):
        '''Обрабатывает подписку пользователя на выбранное издание'''
        # Получаем выбранные строки
        selected_items = publications_table.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "Предупреждение", "Выберите издание для подписки")
            return
        
        # Получаем индекс выбранной строки
        selected_row = publications_table.row(selected_items[0])
        
        # Получаем выбранную публикацию
        selected_publication = self.publications_data[selected_row]
        
        # Проверяем, не подписан ли пользователь уже на это издание
        if self.current_user.has_subscription(publication_id=selected_publication.id):
            QMessageBox.warning(self, "Предупреждение", "Вы уже подписаны на это издание")
            return
        
        # Пытаемся оформить подписку
        success = self.window_controller.subscribe_user_to_publication(
            self.current_user.id, selected_publication.id
        )
        
        if success:
            QMessageBox.information(self, "Успех", f"Вы успешно подписались на издание '{selected_publication.name}'")
            dialog.accept()
            # Обновляем личный кабинет
            self.current_user = self.window_controller.get_user_by_id(self.current_user.id)
            self.refresh_personal_cabinet()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось оформить подписку. Пожалуйста, попробуйте позже.")


    def show_personal_cabinet(self, user):
        """Переключает на личный кабинет пользователя"""
        self.current_user = user
        # Если личный кабинет еще не создан
        if not hasattr(self, 'personal_cabinet_widget'):
            self.personal_cabinet_widget = self.create_personal_cabinet(user)
            self.stacked_widget.addWidget(self.personal_cabinet_widget)
        
        # Показываем личный кабинет
        self.stacked_widget.setCurrentWidget(self.personal_cabinet_widget)
    
    def show_telegram_connect_dialog(self):
        """Показывает диалог с кодом для подключения Telegram-бота"""
        # Создаем диалоговое окно
        dialog = QDialog(self)
        dialog.setWindowTitle("Подключение Telegram-бота")
        dialog.setFixedSize(400, 250)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        # Создаем вертикальный макет для диалога
        layout = QVBoxLayout(dialog)
        
        # Добавляем инструкцию
        instruction_label = QLabel("Для подключения Telegram-бота используйте этот код:")
        instruction_label.setStyleSheet("font-size: 14px; margin-bottom: 15px;")
        instruction_label.setWordWrap(True)
        layout.addWidget(instruction_label)
        
        # Код для бота
        code = generate_auth_code()
        self.bot_controller.active_auth_codes[code] = self.current_user.id
        print(code)
        
        # Создаем QLabel с отображением кода
        code_label = QLabel(str(code))
        code_label.setStyleSheet('''font-size: 24px; margin-bottom: 15px;
                                 border: 1px solid black; border-radius: 5px;''')
        # code_label.setStyleSheet("""
        #     font-size: 24px; 
        #     font-weight: bold; 
        #     padding: 20px; 
        #     background-color: white; 
        #     color: black; 
        #     border: 1px solid #ddd; 
        #     border-radius: 5px; 
        #     margin: 10px 0;
        # """)
        code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # code_label.setTextFormat(Qt.TextFormat.PlainText)  # Устанавливаем формат как обычный текст
        # code_label.adjustSize()  # Подгоняем размер под содержимое
        # code_label.setFixedSize(300, 70)  # Установить фиксированный размер
        code_label.setWordWrap(True)
        layout.addWidget(code_label)
        
        # Добавляем инструкцию по использованию кода
        note_label = QLabel("Откройте бота @magazines_n7_bot в Telegram и введите этот код.")
        note_label.setStyleSheet("font-size: 14px; margin-top: 10px;")
        note_label.setWordWrap(True)
        layout.addWidget(note_label)
        
        # code_debug_label = QLabel(f"Код: {code}")
        # layout.addWidget(code_debug_label)
        
        # Добавляем кнопку "Закрыть"
        close_button = QPushButton("ЗАКРЫТЬ")
        close_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 12px; "
            "font-weight: bold; border-radius: 5px; margin-top: 20px;"
        )
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        
        # Показываем диалог
        dialog.exec()


    def logout(self):
        """Выход из личного кабинета"""
        # Возвращаемся на форму регистрации
        self.current_user = None
        self.login_phone.clear() 
        self.show_register_form()
        print("Пользователь вышел из системы")

    def login_successful(self, user_id):
        """Обработка успешного входа"""
        print("Вход выполнен успешно!")
        
        # Получаем пользователя из контроллера
        self.current_user = self.window_controller.get_user_by_id(user_id)
        
        if not self.current_user:
            print("Ошибка: пользователь не найден")
            return
        
        # Переходим в личный кабинет
        self.show_personal_cabinet(self.current_user)

    def refresh_personal_cabinet(self):
        """Обновляет отображение личного кабинета"""
        if hasattr(self, 'personal_cabinet_widget'):
            # Удаляем текущий виджет из стека
            self.stacked_widget.removeWidget(self.personal_cabinet_widget)
        
        # Создаем новый виджет личного кабинета
        self.personal_cabinet_widget = self.create_personal_cabinet(self.current_user)
        self.stacked_widget.addWidget(self.personal_cabinet_widget)
        self.stacked_widget.setCurrentWidget(self.personal_cabinet_widget)
