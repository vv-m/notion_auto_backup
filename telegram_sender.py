"""
Установить библиотеку "python-telegram-bot":
pip install python-telegram-bot==13.7
Для удобства написана функция, которую можно импортировать.
"""

import os

from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BOT_ID = 6529149049
ADMIN = 247383486
# TELEGRAM_CHANEL = -992292708
bot = Bot(token=TELEGRAM_TOKEN)


# Пример отправки сообщения
# bot.send_message(ADMIN, "Hello world")

# Функции для импорта:
def send_massage_to_admin_telegram(message: str) -> None:
    """ Отправка сообщения Администратору. """
    bot.send_message(ADMIN, message)


def send_massage_to_user_telegram(user: int, message: str) -> None:
    """ Отправка сообщения Пользователю. """
    bot.send_message(user, message)
