class ScoringEngine:

    # ==========================================
    # Creator Score
    # ==========================================

    @staticmethod
    def creator_score(total_token, avg_sol, avg_mc, highest_mc, lowest_mc):

        experience = min(total_token * 2, 30)

        if avg_sol >= 5:
            buy = 25
        elif avg_sol >= 2:
            buy = 20
        elif avg_sol >= 1:
            buy = 15
        elif avg_sol >= 0.5:
            buy = 10
        else:
            buy = 5

        if avg_mc >= 100:
            mc = 30
        elif avg_mc >= 70:
            mc = 25
        elif avg_mc >= 50:
            mc = 20
        elif avg_mc >= 35:
            mc = 15
        else:
            mc = 8

        spread = highest_mc - lowest_mc

        if spread < 5:
            consistency = 15
        elif spread < 20:
            consistency = 10
        else:
            consistency = 5

        final = experience + buy + mc + consistency

        return min(final, 100)

    # ==========================================
    # Risk Score
    # ==========================================

    @staticmethod
    def risk_score(total_token, avg_sol, avg_mc):

        score = 100

        if avg_sol < 0.2:
            score -= 25

        elif avg_sol < 1:
            score -= 10

        if avg_mc < 30:
            score -= 25

        elif avg_mc < 40:
            score -= 10

        if total_token <= 2:
            score -= 15

        return max(score, 0)

    # ==========================================
    # Pattern Score
    # ==========================================

    @staticmethod
    def pattern_score(total_token, highest_mc, lowest_mc):

        score = 100

        spread = highest_mc - lowest_mc

        if spread > 30:
            score -= 40

        elif spread > 15:
            score -= 20

        if total_token < 3:
            score -= 20

        return max(score, 0)

    # ==========================================
    # AI Score
    # ==========================================

    @staticmethod
    def ai_score(creator_score, risk_score, pattern_score):

        score = round(

            creator_score * 0.45 +
            risk_score * 0.35 +
            pattern_score * 0.20

        )

        return score

    # ==========================================
    # Rating
    # ==========================================

    @staticmethod
    def rating(score):

        if score >= 90:
            return "A+"

        elif score >= 80:
            return "A"

        elif score >= 70:
            return "B"

        elif score >= 60:
            return "C"

        else:
            return "D"

    # ==========================================
    # Reputation
    # ==========================================

    @staticmethod
    def reputation(score):

        if score >= 85:
            return "EXCELLENT"

        elif score >= 70:
            return "GOOD"

        elif score >= 55:
            return "FAIR"

        else:
            return "POOR"

    # ==========================================
    # Confidence
    # ==========================================

    @staticmethod
    def confidence(total_token):

        if total_token >= 20:
            return "HIGH"

        elif total_token >= 5:
            return "MEDIUM"

        else:
            return "LOW"