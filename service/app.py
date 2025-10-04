import telebot
import os
from dotenv import load_dotenv

from .handlers import register_handlers
from .background_process import start_roulette
from .database import init_db


def get_token():
    load_dotenv("config.env")
    api_token = os.getenv('TOKEN')
    return api_token


def create_bot():
    api_token = get_token()
    bot = telebot.TeleBot(api_token)
    return bot


def init_app(bot):
    register_handlers(bot)
    init_db()
    start_roulette(bot)
