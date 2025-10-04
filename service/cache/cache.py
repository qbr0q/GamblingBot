from service.database import Session
from service.database.utils import init_user
from .utils import FixesList


class Cache:
    users = {}
    bets = {}
    msg_bet = 0
    bet_history = FixesList(7)

    @classmethod
    def get_or_load(cls, user_id, session=None):
        user = cls.users.get(user_id)
        if not user:
            user = cls._load_user(session, user_id)
            cls.set(user, user_id)
        return user

    @classmethod
    def set(cls, user, user_id):
        cls.users[user_id] = user

    @classmethod
    def set_cache_bet(cls, user_id, cache):
        cls.bets[user_id] = cache

    @classmethod
    def clear_cache(cls):
        cls.bets = {}

    @classmethod
    def set_msg_bet(cls, msg):
        cls.msg_bet = msg

    @classmethod
    def _load_user(cls, session, user_id):
        user = init_user(session, user_id)
        return user

    @classmethod
    def _refresh_cache_user(cls, user):
        cls.users[user.telegram_id] = user

    @classmethod
    def save(cls, user):
        with Session() as session:
            session.expire_on_commit = False
            session.add(user)
            session.commit()
            cls._refresh_cache_user(user)


def load_cache(func):
    def wrapper(message):
        with Session() as session:
            user = Cache.get_or_load(message.from_user.id, session)
            func(message, user)
        Cache.save(user)
    return wrapper
