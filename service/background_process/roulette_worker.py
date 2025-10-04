from time import sleep

from service.cache import Cache
from .utils import get_win_bet, get_random_color, update_bet_history
from settings import group_chat_id, colors_weights
from service.handlers.utils import get_bet_color


def roulette(bot, bets_event):
    while True:

        bet_msg = bot.send_message(group_chat_id, 'Принимаются ставки! (после первой ставки стартует отсчет в 30 секунд)\n'
                                                  'Сделать ставку можно через команду /bet\n'
                                                  f'Черное ({colors_weights["ч"]}%) - х2, '
                                                  f'Красное ({colors_weights["к"]}%) - х3, '
                                                  f'Зеленое ({colors_weights["з"]}%) - х8')
        Cache.msg_bet = bet_msg
        bets_event.wait()
        sleep(30)

        random_color = get_random_color()
        bet_results = []
        if Cache.bets:
            for bet_user, bet_info in Cache.bets.items():
                user = Cache.users.get(bet_user)
                bet_color, bet_rate = bet_info.values()
                bet_result = f"{user.username} -{bet_rate}"
                if bet_color == random_color:
                    win = get_win_bet(bet_color, bet_rate)
                    user.balance += win
                    Cache.save(user)
                    bet_result = f"{user.username} +{win}"
                bet_results.append(bet_result)
        update_bet_history(random_color)
        bot.send_message(group_chat_id,
                         f'Рулетка сыграла - {get_bet_color(random_color)}\n\n' +
                         '\n'.join(bet_results) + '\n\n' +
                         ' '.join(Cache.bet_history[::-1]))

        Cache.clear_cache()
        sleep(1)
        bets_event.clear()
