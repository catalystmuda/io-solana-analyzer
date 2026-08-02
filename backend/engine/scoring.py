class ScoringEngine:


    # ==========================================
    # Creator Score
    # ==========================================

    @staticmethod
    def creator_score(
        total_token,
        avg_sol,
        avg_mc,
        highest_mc,
        lowest_mc
    ):


        score = 0


        # EXPERIENCE

        if total_token <= 5:

            score += total_token * 3


        elif total_token <= 20:

            score += 15 + (total_token - 5)


        elif total_token <= 50:

            score += 25


        else:

            score += 20



        # SOL QUALITY

        if avg_sol >= 10:

            score += 20


        elif avg_sol >= 5:

            score += 18


        elif avg_sol >= 2:

            score += 15


        elif avg_sol >= 1:

            score += 10


        elif avg_sol >= 0.5:

            score += 6


        else:

            score += 2




        # MARKET CAP QUALITY


        if highest_mc >= 500:

            score += 35


        elif highest_mc >= 250:

            score += 30


        elif highest_mc >= 100:

            score += 25


        elif highest_mc >= 50:

            score += 18


        else:

            score += 10




        if avg_mc >= 100:

            score += 20


        elif avg_mc >= 70:

            score += 16


        elif avg_mc >= 50:

            score += 12


        elif avg_mc >= 35:

            score += 8


        else:

            score += 3



        return min(score,100)




    # ==========================================
    # Risk Score
    # ==========================================

    @staticmethod
    def risk_score(
        total_token,
        avg_sol,
        avg_mc
    ):


        score = 100



        if avg_sol < 0.5:

            score -= 25


        elif avg_sol < 1:

            score -= 15




        if avg_mc < 30:

            score -= 25


        elif avg_mc < 50:

            score -= 15




        if total_token > 100:

            score -= 30


        elif total_token > 50:

            score -= 20


        elif total_token >= 30:

            score -= 15




        return max(score,0)




    # ==========================================
    # Pattern Score
    # ==========================================

    @staticmethod
    def pattern_score(
        total_token,
        highest_mc,
        lowest_mc,
        duplicate_name,
        duplicate_symbol,
        unique_mc
    ):


        score = 100



        spread = highest_mc - lowest_mc



        if spread > 30:

            score -= 30


        elif spread > 15:

            score -= 15




        if duplicate_name >= 5:

            score -= 15


        if duplicate_symbol >= 5:

            score -= 15




        if unique_mc <= 3:

            score -= 20




        return max(score,0)




    # ==========================================
    # Behavior Score
    # ==========================================

    @staticmethod
    def behavior_score(
        fast_launch,
        same_sol,
        total_token
    ):


        score = 100



        if fast_launch > 20:

            score -= 40


        elif fast_launch > 10:

            score -= 25


        elif fast_launch > 5:

            score -= 10




        if same_sol:

            score -= 30




        if total_token >= 50:

            score -= 10




        return max(score,0)




    # ==========================================
    # AI FINAL SCORE
    # ==========================================

    @staticmethod
    def ai_score(
        creator_score,
        risk_score,
        pattern_score,
        behavior_score
    ):


        score = round(

            creator_score * 0.30 +

            risk_score * 0.20 +

            pattern_score * 0.20 +

            behavior_score * 0.30

        )


        return max(
            min(score,100),
            0
        )




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