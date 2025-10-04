from random import choices
from service.cache import Cache

from settings import colors_ratio, colors_bet,\
    colors_weights, colors_emoji


def get_win_bet(bet_color, bet_rate):
    ratio = colors_ratio.get(bet_color)
    return bet_rate * ratio


def get_random_color():
    list_colors_weights = colors_weights.values()
    random_color = choices(colors_bet, weights=list_colors_weights, k=1)[0]
    return random_color


def get_color_emoji(random_color):
    color_emoji = colors_emoji.get(random_color)
    return color_emoji


def update_bet_history(random_color):
    color_emoji = get_color_emoji(random_color)
    Cache.bet_history.append(color_emoji)
