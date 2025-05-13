from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class ModeSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор режима")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: #f8f3e6;")
        
        layout = QVBoxLayout(self)
        
        title = QLabel("ГАЗЕТНЫЙ КИОСК")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        label = QLabel("Выберите режим работы:")
        label.setStyleSheet("font-size: 14px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        user_button = QPushButton("Режим пользователя")
        user_button.setStyleSheet(
            "background-color: #1e1e1e; color: white; padding: 10px; "
            "border-radius: 5px; margin: 10px 0;"
        )
        user_button.clicked.connect(self.open_user_mode)
        layout.addWidget(user_button)
        
        admin_button = QPushButton("Режим администратора")
        admin_button.setStyleSheet(
            "background-color: white; color: black; padding: 10px; "
            "border: 1px solid black; border-radius: 5px; margin: 10px 0;"
        )
        admin_button.clicked.connect(self.open_admin_mode)
        layout.addWidget(admin_button)
        
        self.is_admin_mode = False
    
    def open_user_mode(self):
        self.is_admin_mode = False
        self.accept()
    
    def open_admin_mode(self):
        self.is_admin_mode = True
        self.accept()
