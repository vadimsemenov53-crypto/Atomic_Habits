import requests
from config.settings import TELEGRAM_URL, TOKEN_BOT_TG

def send_telegram_message(chat_id, message):
    """ Функция отправка сообщения в телеграм-чат. """
    params = {
        "text": message,
        "chat_id": chat_id,
    }

    requests.get(f"{TELEGRAM_URL}{TOKEN_BOT_TG}/sendMessage", params=params)