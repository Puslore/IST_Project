import asyncio
from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot


load_dotenv()
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = AsyncTeleBot(TELEGRAM_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
async def start_command(message):
    await bot.reply_to(message, "Привет! Я асинхронный бот.")

# Обработчик сообщения "привет"
@bot.message_handler(func=lambda message: message.text.lower() == 'привет')
async def hello_message(message):
    await bot.reply_to(message, f"Привет, {message.from_user.first_name}!")

# Запуск бота
async def start_bot():
    await bot.infinity_polling()
