from app.bot.generate_auth_code import generate_auth_code
from app.database.repositories import (UserRepository,)
from app.database.session import get_session


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
                code = generate_auth_code()
            BotController.active_auth_codes[code] = user_id
        
        return code
    
    def remove_verify_code(self, code: int):
        try:
            del self.active_auth_codes[code]
            return True
        
        except KeyError:
            return False
    
    async def verify_auth_code(self, checking_code: int, tg_chat_id: int) -> bool:
        '''
        Проверяет авторизационный код при подключении бота
        
        Args:
            checking_code (int): Код, введенный пользователем в интерфейсе
            tg_chat_id (int): ID чата пользователя в Telegram
            
        Returns:
            bool: True, если код верный и пользователuserь авторизован, иначе False
        '''
        try:
            if isinstance(checking_code, str):
                checking_code = int(checking_code)
                
            with get_session() as session:
                print(f'{checking_code=}')
                print(f'{self.active_auth_codes[checking_code]=}')
                user = UserRepository(session).find_by_id(self.active_auth_codes[checking_code])
                if checking_code in BotController.active_auth_codes:
                    try:
                        UserRepository(session).update(user.id, **{'tg_chat_id': tg_chat_id})
                        print(f'Added new tg chat id')
                        return True
                    
                    except Exception as err:
                        print(f'Ошибка при добавлении chat id в БД - {err}')
         
        except ValueError:
            print(f'Ошибка: Код "{checking_code}" не является числом')
            return False
        
        except Exception as err:
            print(f'Ошибка при проверке кода: {err}')
            return False

    async def send_login_code(self, checking_code: int, telegram_chat_id: int) -> bool:
        '''
        Проверяет авторизационный код при логине
        
        Args:
            checking_code (int): Код, введенный пользователем в интерфейсе
            telegram_chat_id (int): ID чата пользователя в Telegram
            
        Returns:
            bool: True, если код верный и пользователь авторизован, иначе False
        '''
        try:
            if isinstance(checking_code, str):
                checking_code = int(checking_code)

            # user_id = BotController.active_auth_codes[checking_code]
            print(f'LOGIN CODE - {checking_code}')

            await self.send_notification(telegram_chat_id, str(checking_code))

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
    
    async def send_notification(self, tg_chat_id: int, message: str) -> bool:
        '''
        Отправляет уведомление пользователю через бота
        
        Args:
            tg_chat_id (int): Telegram chat id пользователя
            message (str): Текст сообщения
            
        Returns:
            bool: True, если сообщение отправлено, иначе False
        '''
        from app.bot.bot import bot
        
        print(f'Sending notification to {tg_chat_id=}, message={message[:5]}')
        
        await bot.send_message(tg_chat_id, message)
        
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
