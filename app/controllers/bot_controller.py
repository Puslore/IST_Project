from app.bot.generate_auth_code import generate_auth_code
# from app.database.repositories.user_repository import UserRepository
# from app.database.session import get_session


class BotController:
    '''Контроллер для взаимодействия с Telegram ботом'''
    # {auth code: user id from DB}
    active_auth_codes = {}
    
    def generate_auth_code_for_user(self, user_id: int) -> int:
        '''
        Генерирует код авторизации пользователя
        
        Arguments:
            user_id (int): ID пользователя в базе данных
            
        Returns:
            int: Сгенерированный код авторизации
        '''
        code = generate_auth_code()
        if code not in BotController.active_auth_codes.keys():
            BotController.active_auth_codes[code] = user_id
        else:
            while code in BotController.active_auth_codes.keys():
                code = generate_auth_code
            BotController.active_auth_codes[code] = user_id
        
        return code
    
    async def verify_auth_code(self, checking_code: int, telegram_chat_id: int) -> bool:
        '''
        Проверяет авторизационный код и связывает Telegram ID с пользователем
        
        Args:
            checking_code (int): Код, введенный пользователем в боте
            telegram_chat_id (int): ID чата пользователя в Telegram
            
        Returns:
            bool: True, если код верный и пользователь авторизован, иначе False
        '''
        try:
            if isinstance(checking_code, str):
                checking_code = int(checking_code)

            user_id = BotController.active_auth_codes[checking_code]
            print(f'{checking_code=}')
            if checking_code in BotController.active_auth_codes:
                return True
            
            # TODO добавление chat id пользователя в БД
            # with get_session() as session:
            # Удаление использованного кода из общего словаря
            del BotController.active_auth_codes[checking_code]
                
            #     return True
                
        except ValueError:
            print(f'Ошибка: Код "{checking_code}" не является числом')
            return False
        
        except Exception as err:
            print(f'Ошибка при проверке кода: {err}')
            return False
    
    @classmethod
    def get_active_codes(cls) -> dict:
        '''
        Возвращает словарь активных кодов
        
        Returns:
            dict: Словарь активных кодов {код: user_id}
        '''
        return cls.active_auth_codes
    
    async def send_notification(self, user_id: int, message: str) -> bool:
        '''
        Отправляет уведомление пользователю через бота
        
        Args:
            user_id (int): ID пользователя в базе данных
            message (str): Текст сообщения
            
        Returns:
            bool: True, если сообщение отправлено, иначе False
        '''
        # TODO получение chat id пользователя из БД
        # with get_session() as session:
        #     user_repo = UserRepository(session)
        #     user = user_repo.get_by_id(user_id)
            
        #     if not user or not hasattr(user, 'telegram_chat_id') or not user.telegram_chat_id:
        #         return False
            
            # Здесь должен быть код для отправки сообщения через бота
            # from app.bot.bot import bot
            # await bot.send_message(user.telegram_chat_id, message)
            
            # return True
