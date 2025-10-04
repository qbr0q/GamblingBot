import threading
from .roulette_worker import roulette

bets_event = threading.Event()


def start_roulette(bot):
    roulette_thread = threading.Thread(target=roulette, args=(bot, bets_event))
    roulette_thread.start()
