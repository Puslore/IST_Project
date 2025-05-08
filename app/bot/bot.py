from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from app.controllers.bot_controller import BotController


load_dotenv()
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = AsyncTeleBot(TELEGRAM_TOKEN)
bot_controller = BotController()

user_states = {}
bot_controller.generate_auth_code_for_user(123)
print(bot_controller.get_active_codes())


# Начало диалога
@bot.message_handler(commands=['start'])
async def start_command(message: Message):
    """Обработчик команды /start - запрашивает код авторизации"""
    user_id = message.from_user.id
    user_states[user_id] = 'waiting_for_code'
    
    await bot.send_message(message.chat.id, 
                         "Добро пожаловать в систему авторизации газетного киоска!\n\n"
                         "Пожалуйста, введите код, который вы получили в приложении:")


# Проверка кода
@bot.message_handler(func=lambda message: \
    user_states.get(message.from_user.id) == 'waiting_for_code')
async def auth_code_handler(message: Message):
    """Обработчик получения кода авторизации"""
    chat_id = message.from_user.id
    auth_code = message.text.strip()
    
    # Проверка кода через контроллер бота
    result = await bot_controller.verify_auth_code(checking_code=int(auth_code),
                                                   telegram_chat_id=chat_id)
    
    if result:
        # Успешная авторизация
        user_states[chat_id] = 'authorized'
        await bot.send_message(message.chat.id, 
                             "Авторизация успешна!\n\n"
                             "Теперь вы можете использовать бота для входа в систему.")
    else:
        # Неудачная авторизация
        await bot.send_message(message.chat.id, 
                             "Неверный код авторизации.\n\n"
                             "Пожалуйста, проверьте код и попробуйте снова, "
                             "или вернитесь в приложение для получения нового кода.")


# Запуск бота
async def start_bot():
    await bot.infinity_polling()
