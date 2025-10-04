from service.cache import Cache, load_cache
from .utils import edit_bet_msg, set_default_username
from service.database.utils import get_user_by_username
from settings import admin_ids, known_commands
from service.background_process import bets_event
from service.validation import validation_username, validation_bet


def register_command_handlers(bot):
    @bot.message_handler(commands=['start'])
    @load_cache
    def start(message, user=None):
        bot.send_message(chat_id=message.chat.id,
                         text='Добро пожаловать в мир гемблинга, мир реального дофамина!\n'
                         'Баланс при старте - 10.000\n'
                         'Чтобы установить себе ник, воспользуетесь командой /username {имя}',
                         reply_to_message_id=message.message_id)
        if not user.username:
            set_default_username(user)

    @bot.message_handler(commands=['username'])
    @load_cache
    def set_username(message, user):
        error, username = validation_username(message)
        if not error:
            user.username = username

        bot.send_message(
            chat_id=message.chat.id,
            text=error or 'Ник установлен!',
            reply_to_message_id=message.message_id
        )

    @bot.message_handler(commands=['bet'])
    @load_cache
    def bet(message, user):
        error, bet_rate, bet_color = validation_bet(message, user)

        if not error:
            user.balance -= bet_rate

            Cache.set_cache_bet(user_id=user.telegram_id,
                                cache={'color': bet_color, 'rate': bet_rate})

            msg_edit = edit_bet_msg(bot, user, Cache.msg_bet, bet_rate, bet_color)
            Cache.set_msg_bet(msg_edit)
            bets_event.set()

        bot.send_message(chat_id=message.chat.id,
                         text=error or 'Ставка принята!',
                         reply_to_message_id=message.message_id)

    @bot.message_handler(commands=['balance'])
    @load_cache
    def get_balance(message, user):
        bot.send_message(chat_id=message.chat.id,
                         text=f'Текущий баланс - {user.balance}',
                         reply_to_message_id=message.message_id)

    @bot.message_handler(commands=['set_balance'])
    def set_balance(message):
        if message.from_user.id in admin_ids:
            info = message.text.split()[1:]
            username = ' '.join(info[:-1])
            balance = info[-1]
            user = get_user_by_username(username)
            user.balance = int(balance)
            Cache.save(user)
            bot.send_message(chat_id=message.chat.id,
                             text='Баланс установлен',
                             reply_to_message_id=message.message_id)

    @bot.message_handler(commands=['help'])
    def help(message):
        mess_help = '/username - установить юзернейм (/username name)\n' \
                    '/bet - засандалить сочную ставочку (/bet ставка+цвет)\n' \
                    '/balance - узнать баланс'
        bot.send_message(chat_id=message.chat.id,
                         text=mess_help,
                         reply_to_message_id=message.message_id)

    @bot.message_handler(func=lambda message: message.text.startswith('/'))
    def unknown_command(message):
        if message.text not in known_commands:
            bot.send_message(chat_id=message.chat.id,
                             text=f"Неизвестная команда: {message.text}. "
                                  f"Для помощи воспользуйтесь командой /help",
                             reply_to_message_id=message.message_id)
