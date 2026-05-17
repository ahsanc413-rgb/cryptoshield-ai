class MarketSummaryGenerator:

    def generate_summary(
        self,
        alerts_df,
        trades_df
    ):

        if alerts_df.empty:

            return (
                "Market is currently stable "
                "with no major alerts."
            )

        # Most risky asset
        risky_asset = (
            alerts_df["symbol"]
            .value_counts()
            .idxmax()
        )

        risky_count = (
            alerts_df["symbol"]
            .value_counts()
            .max()
        )

        # Most active asset
        active_asset = (
            trades_df["symbol"]
            .value_counts()
            .idxmax()
        )

        summary = (

            f"{risky_asset} is currently "
            f"showing the highest risk "

            f"with {risky_count} alerts detected. "

            f"{active_asset} is currently "
            f"the most actively traded asset "
            f"in the monitored market."

        )

        return summary