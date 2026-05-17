from collections import defaultdict
from statistics import mean


class PumpDetector:

    def __init__(self):

        self.volume_history = defaultdict(list)

    def detect_pump(self, trade):

        symbol = trade["symbol"]

        quantity = trade["quantity"]

        history = self.volume_history[symbol]

        # Store recent volumes
        history.append(quantity)

        # Keep last 100 trades
        if len(history) > 100:
            history.pop(0)

        # Need enough data
        if len(history) < 20:
            return None

        avg_volume = mean(history)

        # Pump detection
        if quantity > avg_volume * 20:

            return {
                "symbol": symbol,
                "pump_score": round(
                    quantity / avg_volume,
                    2
                ),
                "current_volume": quantity,
                "average_volume": round(
                    avg_volume,
                    4
                )
            }

        return None