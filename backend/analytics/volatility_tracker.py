from collections import defaultdict
from statistics import stdev


class VolatilityTracker:

    def __init__(self):

        self.price_history = defaultdict(list)

    def update(self, trade):

        symbol = trade["symbol"]

        price = trade["price"]

        history = self.price_history[symbol]

        # Store latest prices
        history.append(price)

        # Keep latest 50 prices only
        if len(history) > 50:
            history.pop(0)

        # Need enough data first
        if len(history) < 10:
            return None

        volatility = stdev(history)

        return {
            "symbol": symbol,
            "volatility": round(
                volatility,
                6
            )
        }