from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QLineEdit, QStackedWidget, 
                           QTableWidget, QTableWidgetItem, QFormLayout, 
                           QMessageBox, QHeaderView, QDialog, QComboBox, 
                           QSpinBox, QCheckBox, QDoubleSpinBox, QDateTimeEdit,
                           QScrollArea, QTextEdit)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont

from app.controllers.admin_window_controller import AdminController


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Газетный киоск - Панель администратора")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #f8f3e6;")
        
        self.admin_controller = AdminController()
        self.current_admin = None
        
        # Создаем центральный виджет и стек для переключения между окнами
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Создаем различные виджеты для стека
        self.create_choice_widget()
        self.create_login_widget()
        self.create_registration_widget()
        self.create_admin_dashboard()
        
        # Показываем первый экран
        self.show_choice_screen()
    
    def create_choice_widget(self):
        """Создает виджет выбора входа или регистрации"""
        choice_widget = QWidget()
        layout = QVBoxLayout(choice_widget)
        
        # Заголовок
        title = QLabel("ГАЗЕТНЫЙ КИОСК")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Подзаголовок
        subtitle = QLabel("Панель администратора")
        subtitle.setStyleSheet("font-size: 18px; margin-bottom: 40px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Кнопка входа
        login_button = QPushButton("ВХОД В СИСТЕМУ")
        login_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 15px; "
            "border-radius: 5px; font-size: 16px; margin: 10px 100px;"
        )
        login_button.clicked.connect(self.show_login_screen)
        layout.addWidget(login_button)
        
        # Кнопка регистрации
        register_button = QPushButton("ДОБАВИТЬ АДМИНИСТРАТОРА")
        register_button.setStyleSheet(
            "background-color: white; color: black; padding: 15px; "
            "border: 1px solid black; border-radius: 5px; font-size: 16px; margin: 10px 100px;"
        )
        register_button.clicked.connect(self.show_register_screen)
        layout.addWidget(register_button)
        
        layout.addStretch()
        
        self.choice_widget = choice_widget
        self.stacked_widget.addWidget(choice_widget)
    
    def create_login_widget(self):
        """Создает виджет для входа администратора"""
        login_widget = QWidget()
        layout = QVBoxLayout(login_widget)
        
        # Заголовок
        title = QLabel("ВХОД В СИСТЕМУ")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Форма входа
        form_layout = QFormLayout()
        form_layout.setContentsMargins(100, 20, 100, 20)
        form_layout.setSpacing(20)
        
        # Стиль для полей ввода
        input_style = "padding: 12px; border: 1px solid black; border-radius: 5px; background-color: white;"
        
        # Поле для номера телефона
        self.login_phone = QLineEdit()
        self.login_phone.setStyleSheet(input_style)
        self.login_phone.setPlaceholderText("Введите номер телефона")
        form_layout.addRow("Номер телефона:", self.login_phone)
        
        # Поле для пароля
        self.login_password = QLineEdit()
        self.login_password.setStyleSheet(input_style)
        self.login_password.setPlaceholderText("Введите пароль")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Пароль:", self.login_password)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(100, 20, 100, 20)
        
        # Кнопка входа
        login_button = QPushButton("ВОЙТИ")
        login_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 12px; "
            "border-radius: 5px; font-size: 16px; min-width: 120px;"
        )
        login_button.clicked.connect(self.login_admin)
        buttons_layout.addWidget(login_button)
        
        # Кнопка отмены
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 12px; "
            "border: 1px solid black; border-radius: 5px; font-size: 16px; min-width: 120px;"
        )
        cancel_button.clicked.connect(self.show_choice_screen)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        self.login_widget = login_widget
        self.stacked_widget.addWidget(login_widget)
    
    def create_registration_widget(self):
        """Создает виджет для регистрации нового администратора"""
        register_widget = QWidget()
        layout = QVBoxLayout(register_widget)
        
        # Заголовок
        title = QLabel("ДОБАВЛЕНИЕ АДМИНИСТРАТОРА")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Форма регистрации
        form_layout = QFormLayout()
        form_layout.setContentsMargins(100, 10, 100, 10)
        form_layout.setSpacing(15)
        
        # Стиль для полей ввода
        input_style = "padding: 12px; border: 1px solid black; border-radius: 5px; background-color: white;"
        
        # Поля для ввода данных
        self.first_name_field = QLineEdit()
        self.first_name_field.setStyleSheet(input_style)
        form_layout.addRow("Имя*:", self.first_name_field)
        
        self.last_name_field = QLineEdit()
        self.last_name_field.setStyleSheet(input_style)
        form_layout.addRow("Фамилия*:", self.last_name_field)
        
        self.middle_name_field = QLineEdit()
        self.middle_name_field.setStyleSheet(input_style)
        form_layout.addRow("Отчество:", self.middle_name_field)
        
        self.phone_field = QLineEdit()
        self.phone_field.setStyleSheet(input_style)
        self.phone_field.setPlaceholderText("+7XXXXXXXXXX")
        form_layout.addRow("Телефон*:", self.phone_field)
        
        self.email_field = QLineEdit()
        self.email_field.setStyleSheet(input_style)
        form_layout.addRow("Email:", self.email_field)
        
        self.address_field = QLineEdit()
        self.address_field.setStyleSheet(input_style)
        form_layout.addRow("Адрес*:", self.address_field)
        
        self.salary_field = QDoubleSpinBox()
        self.salary_field.setRange(0, 1000000)
        self.salary_field.setValue(50000)
        self.salary_field.setStyleSheet(input_style)
        form_layout.addRow("Зарплата*:", self.salary_field)
        
        self.password_field = QLineEdit()
        self.password_field.setStyleSheet(input_style)
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Пароль*:", self.password_field)
        
        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setStyleSheet(input_style)
        self.confirm_password_field.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Подтверждение пароля*:", self.confirm_password_field)
        
        layout.addLayout(form_layout)
        
        # Пояснение к обязательным полям
        required_fields = QLabel("* - обязательные поля")
        required_fields.setStyleSheet("font-size: 12px; color: gray;")
        required_fields.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(required_fields, 0, Qt.AlignmentFlag.AlignRight)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(100, 20, 100, 20)
        
        # Кнопка регистрации
        register_button = QPushButton("ДОБАВИТЬ")
        register_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 12px; "
            "border-radius: 5px; font-size: 16px; min-width: 120px;"
        )
        register_button.clicked.connect(self.register_admin)
        buttons_layout.addWidget(register_button)
        
        # Кнопка отмены
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 12px; "
            "border: 1px solid black; border-radius: 5px; font-size: 16px; min-width: 120px;"
        )
        cancel_button.clicked.connect(self.show_choice_screen)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        self.register_widget = register_widget
        self.stacked_widget.addWidget(register_widget)
    
    def create_admin_dashboard(self):
        """Создает главный экран панели администратора"""
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        
        # Верхняя панель с заголовком и кнопкой выхода
        top_layout = QHBoxLayout()
        
        title = QLabel("ПАНЕЛЬ АДМИНИСТРАТОРА")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        top_layout.addWidget(title)
        
        top_layout.addStretch()
        
        self.admin_name_label = QLabel("")
        self.admin_name_label.setStyleSheet("font-size: 16px;")
        top_layout.addWidget(self.admin_name_label)
        
        logout_button = QPushButton("Выйти")
        logout_button.setStyleSheet(
            "background-color: white; color: black; padding: 8px; "
            "border: 1px solid black; border-radius: 5px; min-width: 100px;"
        )
        logout_button.clicked.connect(self.logout)
        top_layout.addWidget(logout_button)
        
        layout.addLayout(top_layout)
        
        # Разделитель
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #ddd;")
        layout.addWidget(separator)
        layout.addSpacing(10)
        
        # Основное содержимое - таблицы и операции
        content_layout = QHBoxLayout()
        
        # Левая панель с кнопками для таблиц
        tables_layout = QVBoxLayout()
        tables_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        tables_label = QLabel("ТАБЛИЦЫ")
        tables_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        tables_layout.addWidget(tables_label)
        
        # Кнопки для просмотра таблиц
        for table_name in ["Пользователи", "Администраторы", "Издательства", 
                          "Публикации", "Выпуски", "Доставщики", "Жалобы", "Доставки"]:
            button = QPushButton(table_name)
            button.setStyleSheet(
                "background-color: white; color: black; padding: 10px; text-align: left; "
                "border: 1px solid #ddd; border-radius: 5px; margin: 3px 0;"
            )
            # Подключаем обработчик со связанными данными через lambda
            button.clicked.connect(lambda checked, name=table_name: self.show_table(name))
            tables_layout.addWidget(button)
        
        content_layout.addLayout(tables_layout)
        
        # Разделитель между панелью кнопок и содержимым
        vseparator = QWidget()
        vseparator.setFixedWidth(1)
        vseparator.setStyleSheet("background-color: #ddd;")
        content_layout.addWidget(vseparator)
        
        # Правая панель с содержимым
        right_panel = QVBoxLayout()
        
        # Заголовок и кнопки операций
        actions_layout = QHBoxLayout()
        
        self.content_title = QLabel("Выберите таблицу")
        self.content_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        actions_layout.addWidget(self.content_title)
        
        actions_layout.addStretch()
        
        # Кнопка добавления записи
        add_record_button = QPushButton("Добавить запись")
        add_record_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 8px; "
            "border-radius: 5px; min-width: 150px;"
        )
        add_record_button.clicked.connect(self.add_record_to_current_table)
        actions_layout.addWidget(add_record_button)
        
        right_panel.addLayout(actions_layout)
        
        # Таблица для отображения данных
        self.data_table = QTableWidget()
        self.data_table.setStyleSheet("background-color: white; border: 1px solid #ddd;")
        right_panel.addWidget(self.data_table)
        
        content_layout.addLayout(right_panel, 3)  # Правая панель занимает больше места
        
        layout.addLayout(content_layout)
        
        self.dashboard_widget = dashboard_widget
        self.stacked_widget.addWidget(dashboard_widget)
    
    def show_choice_screen(self):
        """Показывает экран выбора входа или регистрации"""
        self.stacked_widget.setCurrentWidget(self.choice_widget)
    
    def show_login_screen(self):
        """Показывает экран входа"""
        self.stacked_widget.setCurrentWidget(self.login_widget)
    
    def show_register_screen(self):
        """Показывает экран регистрации"""
        self.stacked_widget.setCurrentWidget(self.register_widget)
    
    def show_dashboard(self):
        """Показывает главный экран панели администратора"""
        self.stacked_widget.setCurrentWidget(self.dashboard_widget)
    
    def login_admin(self):
        """Обрабатывает вход администратора"""
        phone = self.login_phone.text()
        password = self.login_password.text()
        
        if not phone or not password:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все поля")
            return
        
        # Аутентификация администратора через контроллер
        admin = self.admin_controller.authenticate_admin(phone, password)
        
        if admin:
            self.current_admin = admin
            self.admin_name_label.setText(f"Администратор: {admin.get_full_name()}")
            self.show_dashboard()
            self.show_table("Пользователи")  # По умолчанию показываем таблицу пользователей
        else:
            QMessageBox.warning(self, "Ошибка входа", "Неверный номер телефона или пароль")
    
    def register_admin(self):
        """Обрабатывает регистрацию нового администратора"""
        # Собираем данные из формы
        admin_data = {
            'first_name': self.first_name_field.text(),
            'last_name': self.last_name_field.text(),
            'middle_name': self.middle_name_field.text() or None,
            'phone_number': self.phone_field.text(),
            'email': self.email_field.text() or None,
            'address': self.address_field.text(),
            'salary': self.salary_field.value(),
            'password': self.password_field.text()
        }
        
        # Проверка обязательных полей
        required_fields = ['first_name', 'last_name', 'phone_number', 'address', 'password']
        for field in required_fields:
            if not admin_data[field]:
                QMessageBox.warning(self, "Предупреждение", f"Пожалуйста, заполните все обязательные поля")
                return
        
        # Проверка паролей
        if admin_data['password'] != self.confirm_password_field.text():
            QMessageBox.warning(self, "Предупреждение", "Пароли не совпадают")
            return
        
        # Регистрация администратора через контроллер
        success, result = self.admin_controller.create_admin(admin_data)
        
        if success:
            QMessageBox.information(self, "Успех", "Администратор успешно добавлен")
            self.show_choice_screen()
        else:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить администратора: {result}")
    
    def logout(self):
        """Выход из системы"""
        self.current_admin = None
        self.login_phone.clear()
        self.login_password.clear()
        self.show_choice_screen()
    
    def show_table(self, table_name):
        """Отображает выбранную таблицу"""
        self.content_title.setText(f"Таблица: {table_name}")
        
        # Получаем данные таблицы через контроллер
        headers, data = self.admin_controller.get_table_data(table_name)
        
        # Настраиваем таблицу
        self.data_table.setRowCount(len(data))
        self.data_table.setColumnCount(len(headers))
        self.data_table.setHorizontalHeaderLabels(headers)
        
        # Заполняем таблицу данными
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data) if cell_data is not None else "")
                self.data_table.setItem(row_idx, col_idx, item)
        
        # Настраиваем размеры столбцов
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    
    def add_record_to_current_table(self):
        """Добавляет запись в текущую выбранную таблицу"""
        current_table = self.content_title.text().replace("Таблица: ", "")
        
        if current_table == "Выберите таблицу":
            QMessageBox.warning(self, "Предупреждение", "Выберите таблицу для добавления записи")
            return
            
        # Вызываем соответствующий метод в зависимости от выбранной таблицы
        if current_table == "Пользователи":
            self.add_user_dialog()
        elif current_table == "Администраторы":
            self.add_admin_dialog()
        elif current_table == "Издательства":
            self.add_publisher_dialog()
        elif current_table == "Публикации":
            self.show_add_publication_dialog()
        elif current_table == "Выпуски":
            self.show_add_issue_dialog()
        elif current_table == "Доставщики":
            self.add_courier_dialog()
        elif current_table == "Жалобы":
            self.add_complaint_dialog()
        elif current_table == "Доставки":
            self.add_delivery_dialog()
    
    def add_user_dialog(self):
        """Показывает диалог для добавления нового пользователя"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавление пользователя")
        dialog.setFixedWidth(500)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Стиль для полей
        input_style = "padding: 10px; border: 1px solid black; border-radius: 5px; background-color: white;"
        
        # Создаем поля для формы
        first_name_field = QLineEdit()
        first_name_field.setStyleSheet(input_style)
        form_layout.addRow("Имя*:", first_name_field)
        
        last_name_field = QLineEdit()
        last_name_field.setStyleSheet(input_style)
        form_layout.addRow("Фамилия*:", last_name_field)
        
        middle_name_field = QLineEdit()
        middle_name_field.setStyleSheet(input_style)
        form_layout.addRow("Отчество:", middle_name_field)
        
        phone_field = QLineEdit()
        phone_field.setStyleSheet(input_style)
        form_layout.addRow("Телефон*:", phone_field)
        
        email_field = QLineEdit()
        email_field.setStyleSheet(input_style)
        form_layout.addRow("Email:", email_field)
        
        address_field = QLineEdit()
        address_field.setStyleSheet(input_style)
        form_layout.addRow("Адрес*:", address_field)
        
        ad_consent = QCheckBox("Согласие на рекламу")
        form_layout.addRow("Рассылка:", ad_consent)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("СОХРАНИТЬ")
        save_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 10px; "
            "border-radius: 5px; min-width: 100px;"
        )
        
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 10px; "
            "border: 1px solid black; border-radius: 5px; min-width: 100px;"
        )
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        # Соединяем сигналы
        save_button.clicked.connect(lambda: self.save_user(
            dialog,
            first_name_field.text(),
            last_name_field.text(),
            middle_name_field.text(),
            phone_field.text(),
            email_field.text(),
            address_field.text(),
            ad_consent.isChecked()
        ))
        
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def save_user(self, dialog, first_name, last_name, middle_name, phone, email, address, ad_consent):
        """Сохраняет данные нового пользователя"""
        if not first_name or not last_name or not phone or not address:
            QMessageBox.warning(self, "Предупреждение", "Заполните все обязательные поля")
            return
        
        # Создаем объект данных
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name if middle_name else None,
            'phone_number': phone,
            'email': email if email else None,
            'address': address,
            'ad_consent': ad_consent,
            'is_active': True
        }
        
        # Создаем пользователя через контроллер
        success, result = self.admin_controller.create_user(user_data)
        
        if success:
            QMessageBox.information(self, "Успех", "Пользователь успешно добавлен")
            dialog.accept()
            self.show_table("Пользователи")  # Обновляем таблицу
        else:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить пользователя: {result}")
    
    def add_admin_dialog(self):
        """Показывает диалог для добавления нового администратора"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавление администратора")
        dialog.setFixedWidth(500)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Стиль для полей
        input_style = "padding: 10px; border: 1px solid black; border-radius: 5px; background-color: white;"
        
        # Создаем поля для формы
        first_name_field = QLineEdit()
        first_name_field.setStyleSheet(input_style)
        form_layout.addRow("Имя*:", first_name_field)
        
        last_name_field = QLineEdit()
        last_name_field.setStyleSheet(input_style)
        form_layout.addRow("Фамилия*:", last_name_field)
        
        middle_name_field = QLineEdit()
        middle_name_field.setStyleSheet(input_style)
        form_layout.addRow("Отчество:", middle_name_field)
        
        phone_field = QLineEdit()
        phone_field.setStyleSheet(input_style)
        form_layout.addRow("Телефон*:", phone_field)
        
        email_field = QLineEdit()
        email_field.setStyleSheet(input_style)
        form_layout.addRow("Email:", email_field)
        
        address_field = QLineEdit()
        address_field.setStyleSheet(input_style)
        form_layout.addRow("Адрес*:", address_field)
        
        salary_field = QDoubleSpinBox()
        salary_field.setRange(0, 1000000)
        salary_field.setValue(50000)
        salary_field.setStyleSheet(input_style)
        form_layout.addRow("Зарплата*:", salary_field)
        
        password_field = QLineEdit()
        password_field.setStyleSheet(input_style)
        password_field.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Пароль*:", password_field)
        
        confirm_password_field = QLineEdit()
        confirm_password_field.setStyleSheet(input_style)
        confirm_password_field.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Подтверждение пароля*:", confirm_password_field)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("СОХРАНИТЬ")
        save_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 10px; "
            "border-radius: 5px; min-width: 100px;"
        )
        
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 10px; "
            "border: 1px solid black; border-radius: 5px; min-width: 100px;"
        )
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        # Соединяем сигналы
        save_button.clicked.connect(lambda: self.save_admin(
            dialog,
            first_name_field.text(),
            last_name_field.text(),
            middle_name_field.text(),
            phone_field.text(),
            email_field.text(),
            address_field.text(),
            salary_field.value(),
            password_field.text(),
            confirm_password_field.text()
        ))
        
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def save_admin(self, dialog, first_name, last_name, middle_name, phone, email, address, salary, password, confirm_password):
        """Сохраняет данные нового администратора"""
        if not first_name or not last_name or not phone or not address or not password:
            QMessageBox.warning(self, "Предупреждение", "Заполните все обязательные поля")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Предупреждение", "Пароли не совпадают")
            return
        
        # Создаем объект данных
        admin_data = {
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name if middle_name else None,
            'phone_number': phone,
            'email': email if email else None,
            'address': address,
            'salary': salary,
            'password': password,
            'is_active': True
        }
        
        # Создаем администратора через контроллер
        success, result = self.admin_controller.create_admin(admin_data)
        
        if success:
            QMessageBox.information(self, "Успех", "Администратор успешно добавлен")
            dialog.accept()
            self.show_table("Администраторы")  # Обновляем таблицу
        else:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить администратора: {result}")
    
    def add_publisher_dialog(self):
        """Показывает диалог для добавления нового издательства"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавление издательства")
        dialog.setFixedWidth(500)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Стиль для полей
        input_style = "padding: 10px; border: 1px solid black; border-radius: 5px; background-color: white;"
        
        # Создаем поля для формы
        name_field = QLineEdit()
        name_field.setStyleSheet(input_style)
        form_layout.addRow("Название*:", name_field)
        
        owner_field = QLineEdit()
        owner_field.setStyleSheet(input_style)
        form_layout.addRow("Владелец*:", owner_field)
        
        is_active = QCheckBox("Активно")
        is_active.setChecked(True)
        form_layout.addRow("Статус:", is_active)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("СОХРАНИТЬ")
        save_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 10px; "
            "border-radius: 5px; min-width: 100px;"
        )
        
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 10px; "
            "border: 1px solid black; border-radius: 5px; min-width: 100px;"
        )
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        # Соединяем сигналы
        save_button.clicked.connect(lambda: self.save_publisher(
            dialog,
            name_field.text(),
            owner_field.text(),
            is_active.isChecked()
        ))
        
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def save_publisher(self, dialog, name, owner, is_active):
        """Сохраняет данные нового издательства"""
        if not name or not owner:
            QMessageBox.warning(self, "Предупреждение", "Заполните все обязательные поля")
            return
        
        # Создаем объект данных
        publisher_data = {
            'name': name,
            'owner': owner,
            'is_active': is_active
        }
        
        # Создаем издательство через контроллер
        success, result = self.admin_controller.create_publisher(publisher_data)
        
        if success:
            QMessageBox.information(self, "Успех", "Издательство успешно добавлено")
            dialog.accept()
            self.show_table("Издательства")  # Обновляем таблицу
        else:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить издательство: {result}")
    
    def show_add_publication_dialog(self):
        """Показывает диалог для добавления новой публикации"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавление издания")
        dialog.setFixedWidth(500)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Стиль для полей
        input_style = "padding: 10px; border: 1px solid black; border-radius: 5px; background-color: white;"
        
        # Поля для формы
        name_field = QLineEdit()
        name_field.setStyleSheet(input_style)
        form_layout.addRow("Название*:", name_field)
        
        description_field = QLineEdit()
        description_field.setStyleSheet(input_style)
        form_layout.addRow("Описание*:", description_field)
        
        type_combo = QComboBox()
        type_combo.addItems(["газета", "журнал"])
        type_combo.setStyleSheet(input_style)
        form_layout.addRow("Тип издания*:", type_combo)
        
        # Получаем список издательств для выбора
        publishers = self.admin_controller.get_publishers()
        publisher_combo = QComboBox()
        for publisher in publishers:
            publisher_combo.addItem(publisher.name, publisher.id)
        publisher_combo.setStyleSheet(input_style)
        form_layout.addRow("Издательство*:", publisher_combo)
        
        on_sale_check = QCheckBox("В продаже")
        on_sale_check.setChecked(True)
        form_layout.addRow("Статус:", on_sale_check)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("СОХРАНИТЬ")
        save_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 10px; "
            "border-radius: 5px; min-width: 100px;"
        )
        
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 10px; "
            "border: 1px solid black; border-radius: 5px; min-width: 100px;"
        )
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        # Подключаем события
        save_button.clicked.connect(lambda: self.add_publication(
            dialog, 
            name_field.text(), 
            description_field.text(), 
            type_combo.currentText(), 
            publisher_combo.currentData(), 
            on_sale_check.isChecked()
        ))
        
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def add_publication(self, dialog, name, description, pub_type, publisher_id, on_sale):
        """Добавляет новую публикацию"""
        # Проверка обязательных полей
        if not name or not description or not publisher_id:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все обязательные поля")
            return
        
        # Создаем публикацию через контроллер
        publication_data = {
            'name': name,
            'description': description,
            'publication_type': pub_type,
            'publisher_id': publisher_id,
            'on_sale': on_sale
        }
        
        success, result = self.admin_controller.create_publication(publication_data)
        
        if success:
            QMessageBox.information(self, "Успех", "Издание успешно добавлено")
            dialog.accept()
            self.show_table("Публикации")
        else:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить издание: {result}")
    
    def show_add_issue_dialog(self):
        """Показывает диалог для добавления нового выпуска"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавление выпуска")
        dialog.setFixedWidth(500)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Стиль для полей
        input_style = "padding: 10px; border: 1px solid black; border-radius: 5px; background-color: white;"
        
        # Получаем список публикаций для выбора
        publications = self.admin_controller.get_publications()
        publication_combo = QComboBox()
        for pub in publications:
            publication_combo.addItem(f"{pub.name} ({pub.publication_type})", pub.id)
        publication_combo.setStyleSheet(input_style)
        form_layout.addRow("Издание*:", publication_combo)
        
        name_field = QLineEdit()
        name_field.setStyleSheet(input_style)
        form_layout.addRow("Название выпуска*:", name_field)
        
        description_field = QLineEdit()
        description_field.setStyleSheet(input_style)
        form_layout.addRow("Описание*:", description_field)
        
        issue_number = QSpinBox()
        issue_number.setRange(1, 10000)
        issue_number.setStyleSheet(input_style)
        form_layout.addRow("Номер выпуска*:", issue_number)
        
        issue_date = QDateTimeEdit()
        issue_date.setDateTime(QDateTime.currentDateTime())
        issue_date.setStyleSheet(input_style)
        form_layout.addRow("Дата выпуска*:", issue_date)
        
        cost_field = QDoubleSpinBox()
        cost_field.setRange(0, 10000)
        cost_field.setValue(100)
        cost_field.setStyleSheet(input_style)
        form_layout.addRow("Стоимость*:", cost_field)
        
        special_edition = QCheckBox("Специальный выпуск")
        form_layout.addRow("Спец. выпуск:", special_edition)
        
        on_sale_check = QCheckBox("В продаже")
        on_sale_check.setChecked(True)
        form_layout.addRow("Статус:", on_sale_check)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("СОХРАНИТЬ")
        save_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 10px; "
            "border-radius: 5px; min-width: 100px;"
        )
        
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 10px; "
            "border: 1px solid black; border-radius: 5px; min-width: 100px;"
        )
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        # Подключаем события
        save_button.clicked.connect(lambda: self.add_issue(
            dialog, 
            name_field.text(), 
            description_field.text(), 
            issue_number.value(), 
            issue_date.dateTime().toString('yyyy-MM-dd HH:mm:ss'),
            publication_combo.currentData(), 
            cost_field.value(),
            special_edition.isChecked(), 
            on_sale_check.isChecked()
        ))
        
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def add_issue(self, dialog, name, description, issue_number, issue_date, 
                 publication_id, cost, is_special_edition, on_sale):
        """Добавляет новый выпуск"""
        # Проверка обязательных полей
        if not name or not description or not publication_id:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все обязательные поля")
            return
        
        # Получаем тип публикации
        publication_type = self.admin_controller.get_publication_type(publication_id)
        
        # Создаем выпуск через контроллер
        issue_data = {
            'name': name,
            'description': description,
            'issue_number': issue_number,
            'issue_date': issue_date,
            'publication_series_id': publication_id,
            'issue_type': publication_type,
            'cost': cost,
            'is_special_edition': is_special_edition,
            'on_sale': on_sale
        }
        
        success, result = self.admin_controller.create_issue(issue_data)
        
        if success:
            QMessageBox.information(self, "Успех", "Выпуск успешно добавлен")
            dialog.accept()
            self.show_table("Выпуски")
        else:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить выпуск: {result}")
    
    def add_courier_dialog(self):
        """Показывает диалог для добавления нового курьера"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавление курьера")
        dialog.setFixedWidth(500)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Стиль для полей
        input_style = "padding: 10px; border: 1px solid black; border-radius: 5px; background-color: white;"
        
        # Поля для формы
        first_name_field = QLineEdit()
        first_name_field.setStyleSheet(input_style)
        form_layout.addRow("Имя*:", first_name_field)
        
        last_name_field = QLineEdit()
        last_name_field.setStyleSheet(input_style)
        form_layout.addRow("Фамилия*:", last_name_field)
        
        middle_name_field = QLineEdit()
        middle_name_field.setStyleSheet(input_style)
        form_layout.addRow("Отчество:", middle_name_field)
        
        phone_field = QLineEdit()
        phone_field.setStyleSheet(input_style)
        form_layout.addRow("Телефон*:", phone_field)
        
        email_field = QLineEdit()
        email_field.setStyleSheet(input_style)
        form_layout.addRow("Email:", email_field)
        
        address_field = QLineEdit()
        address_field.setStyleSheet(input_style)
        form_layout.addRow("Адрес*:", address_field)
        
        salary_field = QDoubleSpinBox()
        salary_field.setRange(0, 500000)
        salary_field.setValue(35000)
        salary_field.setStyleSheet(input_style)
        form_layout.addRow("Зарплата*:", salary_field)
        
        rating_field = QDoubleSpinBox()
        rating_field.setRange(0, 5)
        rating_field.setValue(5)
        rating_field.setSingleStep(0.1)
        rating_field.setStyleSheet(input_style)
        form_layout.addRow("Рейтинг:", rating_field)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("СОХРАНИТЬ")
        save_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 10px; "
            "border-radius: 5px; min-width: 100px;"
        )
        
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 10px; "
            "border: 1px solid black; border-radius: 5px; min-width: 100px;"
        )
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        # Соединяем сигналы
        save_button.clicked.connect(lambda: self.save_courier(
            dialog,
            first_name_field.text(),
            last_name_field.text(),
            middle_name_field.text(),
            phone_field.text(),
            email_field.text(),
            address_field.text(),
            salary_field.value(),
            rating_field.value()
        ))
        
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def save_courier(self, dialog, first_name, last_name, middle_name, phone, email, address, salary, rating):
        """Сохраняет данные нового курьера"""
        if not first_name or not last_name or not phone or not address:
            QMessageBox.warning(self, "Предупреждение", "Заполните все обязательные поля")
            return
        
        # Создаем объект данных
        courier_data = {
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name if middle_name else None,
            'phone_number': phone,
            'email': email if email else None,
            'address': address,
            'salary': salary,
            'rating': rating,
            'is_active': True
        }
        
        # Создаем курьера через контроллер
        success, result = self.admin_controller.create_courier(courier_data)
        
        if success:
            QMessageBox.information(self, "Успех", "Курьер успешно добавлен")
            dialog.accept()
            self.show_table("Доставщики")  # Обновляем таблицу
        else:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить курьера: {result}")
    
    def add_complaint_dialog(self):
        """Показывает диалог для добавления новой жалобы"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавление жалобы")
        dialog.setFixedWidth(500)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Стиль для полей
        input_style = "padding: 10px; border: 1px solid black; border-radius: 5px; background-color: white;"
        
        # Получаем список курьеров для выбора
        couriers = self.admin_controller.get_couriers()
        courier_combo = QComboBox()
        for courier in couriers:
            courier_combo.addItem(f"{courier.first_name} {courier.last_name}", courier.id)
        courier_combo.setStyleSheet(input_style)
        form_layout.addRow("Доставщик*:", courier_combo)
        
        description_field = QTextEdit()
        description_field.setStyleSheet(input_style)
        description_field.setMinimumHeight(100)
        form_layout.addRow("Описание жалобы*:", description_field)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("СОХРАНИТЬ")
        save_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 10px; "
            "border-radius: 5px; min-width: 100px;"
        )
        
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 10px; "
            "border: 1px solid black; border-radius: 5px; min-width: 100px;"
        )
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        # Соединяем сигналы
        save_button.clicked.connect(lambda: self.save_complaint(
            dialog,
            courier_combo.currentData(),
            description_field.toPlainText()
        ))
        
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def save_complaint(self, dialog, courier_id, description):
        """Сохраняет данные новой жалобы"""
        if not courier_id or not description:
            QMessageBox.warning(self, "Предупреждение", "Заполните все обязательные поля")
            return
        
        # Создаем объект данных
        complaint_data = {
            'courier_id': courier_id,
            'description': description
        }
        
        # Создаем жалобу через контроллер
        success, result = self.admin_controller.create_complaint(complaint_data)
        
        if success:
            QMessageBox.information(self, "Успех", "Жалоба успешно добавлена")
            dialog.accept()
            self.show_table("Жалобы")  # Обновляем таблицу
        else:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить жалобу: {result}")
    
    def add_delivery_dialog(self):
        """Показывает диалог для добавления новой доставки"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавление доставки")
        dialog.setFixedWidth(500)
        dialog.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Стиль для полей
        input_style = "padding: 10px; border: 1px solid black; border-radius: 5px; background-color: white;"
        
        # Получаем список выпусков для выбора
        issues = self.admin_controller.get_issues()
        issue_combo = QComboBox()
        for issue in issues:
            issue_combo.addItem(f"{issue.name} (№{issue.issue_number})", issue.id)
        issue_combo.setStyleSheet(input_style)
        form_layout.addRow("Выпуск*:", issue_combo)
        
        # Получаем список курьеров
        couriers = self.admin_controller.get_couriers()
        courier_combo = QComboBox()
        for courier in couriers:
            courier_combo.addItem(f"{courier.first_name} {courier.last_name}", courier.id)
        courier_combo.setStyleSheet(input_style)
        form_layout.addRow("Курьер*:", courier_combo)
        
        recipient_field = QLineEdit()
        recipient_field.setStyleSheet(input_style)
        form_layout.addRow("Получатель*:", recipient_field)
        
        recipient_phone_field = QLineEdit()
        recipient_phone_field.setStyleSheet(input_style)
        recipient_phone_field.setPlaceholderText("+7XXXXXXXXXX")
        form_layout.addRow("Телефон получателя*:", recipient_phone_field)
        
        address_field = QLineEdit()
        address_field.setStyleSheet(input_style)
        form_layout.addRow("Адрес доставки*:", address_field)
        
        # Опциональное поле для Telegram ID получателя
        tg_chat_id_field = QLineEdit()
        tg_chat_id_field.setStyleSheet(input_style)
        form_layout.addRow("TG Chat ID получателя:", tg_chat_id_field)
        
        delivery_date = QDateTimeEdit()
        delivery_date.setDateTime(QDateTime.currentDateTime())
        delivery_date.setStyleSheet(input_style)
        form_layout.addRow("Дата доставки:", delivery_date)
        
        is_delivered = QCheckBox("Доставлено")
        form_layout.addRow("Статус:", is_delivered)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("СОХРАНИТЬ")
        save_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 10px; "
            "border-radius: 5px; min-width: 100px;"
        )
        
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet(
            "background-color: white; color: black; padding: 10px; "
            "border: 1px solid black; border-radius: 5px; min-width: 100px;"
        )
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        # Соединяем сигналы
        save_button.clicked.connect(lambda: self.save_delivery(
            dialog,
            issue_combo.currentData(),
            courier_combo.currentData(),
            recipient_field.text(),
            recipient_phone_field.text(),
            address_field.text(),
            tg_chat_id_field.text() if tg_chat_id_field.text() else None,
            delivery_date.dateTime().toString('yyyy-MM-dd HH:mm:ss'),
            is_delivered.isChecked()
        ))
        
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()

    
    def save_delivery(self, dialog, issue_id, courier_id, recipient_name, recipient_phone, 
                    recipient_address, recipient_tg_chat_id, delivery_date, is_delivered):
        """Сохраняет данные новой доставки"""
        if not issue_id or not courier_id or not recipient_name or not recipient_phone or not recipient_address:
            QMessageBox.warning(self, "Предупреждение", "Заполните все обязательные поля")
            return
        
        # Получаем информацию о выпуске для определения стоимости и типа
        issue = self.admin_controller.get_issue_by_id(issue_id)
        if not issue:
            QMessageBox.warning(self, "Ошибка", f"Не удалось найти выпуск с ID {issue_id}")
            return
        
        # Создаем объект данных для доставки
        delivery_data = {
            'item_id': issue_id,
            'item_type': issue.issue_type,
            'courier_id': courier_id,
            'recipient_name': recipient_name,
            'recipient_address': recipient_address,
            'recipient_phone': recipient_phone,
            'item_cost': issue.cost,
            'is_delivered': is_delivered
        }
        
        # Добавляем опциональные данные
        if recipient_tg_chat_id:
            try:
                delivery_data['recipient_tg_chat_id'] = int(recipient_tg_chat_id)
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "ID чата Telegram должен быть числом")
                return
        
        # Добавляем дату доставки, если доставка уже выполнена
        if is_delivered:
            delivery_data['delivery_date'] = delivery_date
        
        # Создаем доставку через контроллер
        success, result = self.admin_controller.create_delivery(delivery_data)
        
        if success:
            QMessageBox.information(self, "Успех", "Доставка успешно добавлена")
            dialog.accept()
            self.show_table("Доставки")
        else:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить доставку: {result}")
