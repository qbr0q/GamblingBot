from service.database.utils import get_all_usernames
from service.handlers.utils import is_enough_balance
from service.cache import Cache


def validation_username(message):
    error = ''
    mess_text = message.text.split()
    if len(mess_text) < 2:
        error = 'Ник ставится командой /username {ник}'
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
        error = 'Ставка приниматся в виде: /bet {ставка}{к, ч, з}'
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
