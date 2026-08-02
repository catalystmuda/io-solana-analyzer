import sqlite3




class CreatorCalibrationV2:


    def __init__(self):


        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )


        self.cursor = self.conn.cursor()




    # =====================================
    # ANALYZE CREATOR CALIBRATION V2
    # =====================================


    def analyze(self, creator):


        self.cursor.execute(
            """
            SELECT
                COUNT(*),
                MAX(market_cap_sol),
                AVG(market_cap_sol)
            FROM tokens
            WHERE creator = ?
            """,
            (creator,)
        )


        row = self.cursor.fetchone()



        if not row or row[0] == 0:

            return None



        total_token = row[0] or 0

        highest_mc = row[1] or 0

        average_mc = row[2] or 0




        # =====================================
        # SURVIVAL CHECK
        # =====================================


        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM tokens
            WHERE creator = ?
            AND market_cap_sol >= 100
            """,
            (creator,)
        )


        survivor = self.cursor.fetchone()[0]





        # =====================================
        # BREAKOUT CHECK
        # =====================================


        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM tokens
            WHERE creator = ?
            AND market_cap_sol >= 500
            """,
            (creator,)
        )


        breakout = self.cursor.fetchone()[0]






        # =====================================
        # MARKET QUALITY
        # =====================================


        market_score = 0



        if highest_mc >= 1000:

            market_score = 35


        elif highest_mc >= 500:

            market_score = 30


        elif highest_mc >= 100:

            market_score = 20


        else:

            market_score = 5






        # =====================================
        # SUCCESS SIGNAL
        # =====================================


        success_score = 0



        if breakout >= 1:


            success_score += 30



        if survivor >= 1:


            success_score += 20



        success_score = min(
            success_score,
            30
        )






        # =====================================
        # SURVIVAL SCORE
        # =====================================


        survival_score = 0



        if survivor >= 3:


            survival_score = 20


        elif survivor >= 1:


            survival_score = 15


        else:

            survival_score = 0






        # =====================================
        # HISTORY SCORE
        # =====================================


        history_score = 0



        if total_token >= 50:


            history_score = 15


        elif total_token >= 10:


            history_score = 12


        elif total_token >= 3:


            history_score = 8


        else:


            history_score = 5






        # =====================================
        # EARLY CREATOR BONUS
        # =====================================


        early_bonus = 0



        if total_token <= 3 and breakout >= 1:


            early_bonus = 10






        final_score = (

            market_score

            +

            success_score

            +

            survival_score

            +

            history_score

            +

            early_bonus

        )



        final_score = min(
            final_score,
            100
        )






        reasons = []



        if breakout > 0:


            reasons.append(
                "Breakout token detected"
            )



        if survivor > 0:


            reasons.append(
                "Survival token detected"
            )



        if total_token <= 3:


            reasons.append(
                "Early creator profile"
            )



        if total_token >= 30:


            reasons.append(
                "Large creator history"
            )



        if average_mc < 50:


            reasons.append(
                "Low average marketcap"
            )



        if not reasons:


            reasons.append(
                "Neutral creator signal"
            )






        return {


            "creator": creator,

            "calibration_score": final_score,

            "total_token": total_token,

            "highest_mc": highest_mc,

            "average_mc": average_mc,

            "survivor": survivor,

            "breakout": breakout,

            "market_score": market_score,

            "success_score": success_score,

            "survival_score": survival_score,

            "history_score": history_score,

            "early_bonus": early_bonus,

            "reasons": reasons

        }






    def close(self):


        self.conn.close()






# =====================================
# TEST
# =====================================


if __name__ == "__main__":



    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorCalibrationV2()



    result = engine.analyze(
        creator
    )



    print()


    print("==============================")

    print(" CREATOR CALIBRATION V2 ")

    print("==============================")



    if result is None:


        print(
            "Creator tidak ditemukan"
        )


    else:


        print(
            f"Creator          : {result['creator']}"
        )


        print("--------------------------------")


        print(
            f"Calibration V2   : {result['calibration_score']}/100"
        )


        print(
            f"Total Token      : {result['total_token']}"
        )


        print(
            f"Highest MC       : {result['highest_mc']:.2f}"
        )


        print(
            f"Average MC       : {result['average_mc']:.2f}"
        )


        print("--------------------------------")


        print(
            f"Survivor         : {result['survivor']}"
        )


        print(
            f"Breakout         : {result['breakout']}"
        )


        print("--------------------------------")


        print(
            "REASONS"
        )


        for r in result["reasons"]:


            print(
                "-",
                r
            )



    engine.close()