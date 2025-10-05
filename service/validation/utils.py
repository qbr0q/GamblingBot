from service.database.utils import get_all_usernames
from service.handlers.utils import is_enough_balance
from service.cache import Cache


def validation_username(message, user):
    error = ''
    mess_text = message.text.split()
    if len(mess_text) == 1:
        error = f'Текущий юзернейм - {user.username}.\n' \
                'Для установки нового юзернейма, воспользуйтесь /username {username}'
    username = ' '.join(mess_text[1:])
    all_usernames = get_all_usernames()
    if username in all_usernames:
        error = 'Ник уже занят'

    return error, username


def validation_bet(message, user):
    error, bet_rate_str, bet_color = '', '', ''
    bet_rate = 0
    mess_text = message.text.split()

    if len(mess_text) != 2 or len(mess_text[1]) < 2:
        error = 'Ставка приниматся в виде: /bet {ставка}{к, ч, з}. Пример - /bet 1000к'
    bet = mess_text[-1]
    bet_rate_str, bet_color = bet[:-1], bet[-1]
    if not error and (not bet_rate_str.isdigit() or bet_color not in ('к', 'ч', 'з') or int(bet_rate_str) == 0):
        error = 'Число - целое положительное число\n' \
                'Цвет - вводится в формате одной из трех букв (к, ч, з)'
    if not error:
        if Cache.bets.get(user.telegram_id):
            error = 'Нельзя сделать ставку второй раз'
        else:
            bet_rate = int(bet_rate_str)
            if not is_enough_balance(user.balance, bet_rate):
                error = 'Недостаточно средств на балансе'

    return error, bet_rate, bet_color   


def validation_give(message, user):
    amount = 0

    if not message.reply_to_message:
        return 'Ответь на сообщение пользователя, которому хочешь передать деньги.', amount
    mess_text = message.text.split()
    if len(mess_text) != 2:
        return 'Передача средств работает в виде /give {сумма}.' \
               'Пример - /give 1000', amount
    amount_str = mess_text[-1]
    if not amount_str.isdigit():
        return 'Некорректная сумма', amount
    amount = int(amount_str)
    if not is_enough_balance(user.balance, amount):
        return 'Недостаточно средств на балансе', amount, recipient_username
    return '', amount
