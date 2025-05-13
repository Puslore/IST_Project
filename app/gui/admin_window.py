from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QLineEdit, QStackedWidget, 
                           QTableWidget, QTableWidgetItem, QFormLayout, 
                           QMessageBox, QHeaderView, QDialog, QComboBox, 
                           QSpinBox, QCheckBox, QDoubleSpinBox, QDateTimeEdit)
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
        
        # Кнопка добавления публикации
        add_publication_button = QPushButton("Добавить издание")
        add_publication_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 8px; "
            "border-radius: 5px; min-width: 150px;"
        )
        add_publication_button.clicked.connect(self.show_add_publication_dialog)
        actions_layout.addWidget(add_publication_button)
        
        # Кнопка добавления выпуска
        add_issue_button = QPushButton("Добавить выпуск")
        add_issue_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 8px; "
            "border-radius: 5px; min-width: 150px;"
        )
        add_issue_button.clicked.connect(self.show_add_issue_dialog)
        actions_layout.addWidget(add_issue_button)
        
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
            dialog, name_field.text(), description_field.text(), 
            type_combo.currentText(), publisher_combo.currentData(), 
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
            dialog, name_field.text(), description_field.text(), 
            issue_number.value(), issue_date.dateTime().toString('yyyy-MM-dd HH:mm:ss'),
            publication_combo.currentData(), cost_field.value(),
            special_edition.isChecked(), on_sale_check.isChecked()
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
            'publication_type': publication_type,
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
