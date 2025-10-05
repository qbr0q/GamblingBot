from settings import colors_name, group_chat_id


def edit_bet_msg(bot, user, msg_bet, bet_rate, bet_color):
    sep = '\n' if msg_bet.edit_date else '\n\n'
    new_text = msg_bet.text + f'{sep}{user.username or user.telegram_id}' \
                              f' - {bet_rate} {get_bet_color(bet_color)}'
    msg_edit = bot.edit_message_text(
        chat_id=group_chat_id,
        message_id=msg_bet.message_id,
        text=new_text
    )
    return msg_edit


def get_bet_color(bet_color):
    return colors_name.get(bet_color)


def is_enough_balance(balance, amount):
    return balance >= amount


def set_default_username(user):
    user.username = f"лудик №{user.id}"
