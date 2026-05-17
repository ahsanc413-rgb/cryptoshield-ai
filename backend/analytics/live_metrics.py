from collections import defaultdict


class LiveMetrics:

    def __init__(self):

        self.trade_count = defaultdict(int)

        self.total_volume = defaultdict(float)

        self.last_price = {}

        self.price_change = defaultdict(float)

    def update_metrics(self, trade):

        symbol = trade["symbol"]

        price = trade["price"]

        quantity = trade["quantity"]

        # Count trades
        self.trade_count[symbol] += 1

        # Add total volume
        self.total_volume[symbol] += quantity

        # Track price changes
        if symbol in self.last_price:

            old_price = self.last_price[symbol]

            change_percent = (
                (price - old_price) / old_price
            ) * 100

            self.price_change[symbol] = change_percent

        self.last_price[symbol] = price

    def get_summary(self):

        summary = []

        for symbol in self.trade_count:

            summary.append({
                "symbol": symbol,
                "trades": self.trade_count[symbol],
                "volume": round(
                    self.total_volume[symbol], 4
                ),
                "price_change_percent": round(
                    self.price_change[symbol], 5
                )
            })

        return summary