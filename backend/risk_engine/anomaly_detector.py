from collections import defaultdict
from statistics import mean


class AnomalyDetector:

    def __init__(self):

        self.trade_history = defaultdict(list)

    def analyze_trade(self, trade):

        symbol = trade["symbol"]

        quantity = trade["quantity"]

        history = self.trade_history[symbol]

        # Store recent quantities
        history.append(quantity)

        # Keep only recent 100 trades
        if len(history) > 100:
            history.pop(0)

        # Need enough data first
        if len(history) < 20:
            return None

        avg_quantity = mean(history)

        # Whale detection
        if quantity > avg_quantity * 10:

            return {
                "symbol": symbol,
                "alert_type": "WHALE_ACTIVITY",
                "trade_quantity": quantity,
                "average_quantity": round(avg_quantity, 4)
            }

        return None