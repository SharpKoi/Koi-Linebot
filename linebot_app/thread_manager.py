import threading
from typing import Set

_thread_pool: Set[threading.Thread] = set()
_death_pill = threading.Event()


def thread(daemon: bool):
    def decorator(func):
        _thread_pool.add(threading.Thread(target=func, daemon=daemon, args=(_death_pill,)))
        return func

    return decorator


def run_all():
    for th in _thread_pool:
        th.start()


def stop_all():
    _death_pill.set()
