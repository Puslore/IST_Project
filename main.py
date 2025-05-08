from app.database import session


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
            return True
        
        else:
            return True
    
    else:
        return True


def create_gui():
    ...


def start_app():
    create_gui()


def main():
    create_db(False)
    start_app()


if __name__ == "__main__":
    PATH = ''
    main(PATH)