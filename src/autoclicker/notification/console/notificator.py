"""
Console notificator
"""
from datetime import datetime

from ..utility import clear_screen, History


STABLE_SYMBOL = "•"
UP_SYMBOL = "🠕"
DOWN_SYMBOL = "🠗"


class ConsoleNotificator:
    def __init__(self):
        self._start_time = datetime.now().strftime('%H:%M %d.%m')
        self._initial_total_coins = None
        self._history = History(50)

    def _avg_chart(self):
        if len(self._history) < 2:
            return STABLE_SYMBOL

        last = float(self._history[len(self._history) - 1])
        other = [float(elem) for elem in self._history[:len(self._history) - 2]]
        length = len(other)

        if length == 0:
            return STABLE_SYMBOL

        if sum(other) / length < last:
            return UP_SYMBOL

        if sum(other) / length > last:
            return DOWN_SYMBOL

        return "•"

    def _chart(self) -> str:
        if len(self._history) < 2:
            return STABLE_SYMBOL

        first = float(self._history[len(self._history) - 2])
        last = float(self._history[len(self._history) - 1])

        if first > last:
            return DOWN_SYMBOL

        if first < last:
            return UP_SYMBOL

        return STABLE_SYMBOL

    def update(self, **kwargs):
        """
        Update console notificator
        """
        clear_screen()
        total = kwargs.get('total')
        earn = kwargs.get('earn') if kwargs.get('earn') is not None else 0

        if self._initial_total_coins is None:
            self._initial_total_coins = kwargs.get('total')

        self._history.append(earn)
        print()
        print("--- BeerTap Game Console notification ---")
        print(f"--- Miner start time: {self._start_time}")
        print(f"--- Initial coins count: {self._initial_total_coins}")
        print(f"--- Coins: {total} (+{earn})")
        print(f"--- Chart: last - {self._chart()} average - {self._avg_chart()}")
