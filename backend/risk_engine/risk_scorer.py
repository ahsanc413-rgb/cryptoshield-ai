class RiskScorer:

    def calculate_risk(self, trade, alert):

        score = 0

        quantity = trade["quantity"]

        # Whale activity contribution
        if alert:

            score += 50

        # Trade size scoring
        if quantity > 1000:
            score += 25

        elif quantity > 100:
            score += 15

        elif quantity > 10:
            score += 5

        # Determine risk level
        if score >= 75:
            level = "EXTREME"

        elif score >= 50:
            level = "HIGH"

        elif score >= 25:
            level = "MEDIUM"

        else:
            level = "LOW"

        return {
            "score": score,
            "level": level
        }