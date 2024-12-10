from telebot.async_telebot import AsyncTeleBot

from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()
# Получаем токен из переменных окружения
TOKEN = os.getenv('TOKEN')

# Создаем экземпляр бота с использованием токена
bot = AsyncTeleBot(TOKEN)  # токен


