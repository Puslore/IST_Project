import sys
import asyncio
import qtinter
from PyQt6.QtWidgets import QApplication
from app.gui.user_window import Main_Window
from app.bot.bot import start_bot
from app.database.init_db import init_db
from utilities import fill_db


def create_db(skip_test_filling: bool = True) -> bool:
    '''
    Создание и инициализация базы данных.
    
    Attributes:
        skip_test_filling (bool): при передаче False, наполняет БД тестовыми данными

    Returns:
        bool: True, если БД успешно создана
    '''
    exist = False
    if not exist:
        if not skip_test_filling:
            fill_db()
            init_db()
            return True
    
        else:
            init_db()
            return True
    
    else:
        return True


def start_app():
    '''
    Функция, запускающая работу приложения
    '''
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    
    # Запуск PyQt и бота вместе
    with qtinter.using_asyncio_from_qt():
        asyncio.create_task(start_bot())
        app.exec()


def main():
    # create_db()
    start_app()


if __name__ == "__main__":
    main()