import sqlite3


class CreatorSurvival:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()



    # ==========================================
    # CALCULATE
    # COMPATIBILITY FOR INTELLIGENCE ENGINE
    # ==========================================

    def calculate(self, creator):

        return self.analyze(creator)



    # ==========================================
    # ANALYZE CREATOR SURVIVAL
    # ==========================================

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



        if row is None or row[0] == 0:

            return None



        total_token = row[0] or 0

        highest_mc = row[1] or 0

        avg_mc = row[2] or 0



        # ======================================
        # SURVIVOR TOKEN
        # MC >= 100 SOL
        # ======================================


        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM tokens
            WHERE creator = ?
            AND market_cap_sol >= 100
            """,
            (creator,)
        )


        survivor_token = self.cursor.fetchone()[0]



        # ======================================
        # BREAKOUT TOKEN
        # MC >= 500 SOL
        # ======================================


        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM tokens
            WHERE creator = ?
            AND market_cap_sol >= 500
            """,
            (creator,)
        )


        breakout_token = self.cursor.fetchone()[0]



        dead_token = total_token - survivor_token



        # ======================================
        # SUCCESS RATE
        # ======================================


        success_rate = round(

            (survivor_token / total_token) * 100,

            2

        )



        # ======================================
        # SURVIVAL SCORE
        # ======================================


        score = 0



        if success_rate >= 50:

            score += 40


        elif success_rate >= 20:

            score += 25


        elif success_rate >= 10:

            score += 10



        # breakout

        if breakout_token >= 3:

            score += 40


        elif breakout_token >= 1:

            score += 25



        # average market cap

        if avg_mc >= 100:

            score += 20


        elif avg_mc >= 50:

            score += 10



        score = min(score,100)



        # ======================================
        # REASONS
        # ======================================


        reasons = []


        if survivor_token == 0:

            reasons.append(
                "Tidak ada token dengan market cap kuat"
            )



        if breakout_token == 0:

            reasons.append(
                "Belum ada token breakout"
            )



        if total_token >= 30:

            reasons.append(
                "Creator melakukan banyak launch"
            )



        if success_rate < 10:

            reasons.append(
                "Mayoritas token gagal berkembang"
            )



        if not reasons:

            reasons.append(
                "Creator memiliki survival bagus"
            )



        return {


            "creator": creator,

            "total_token": total_token,

            "survivor_token": survivor_token,

            "dead_token": dead_token,

            "success_rate": success_rate,

            "breakout_token": breakout_token,

            "highest_mc": highest_mc,

            "avg_mc": avg_mc,

            "survival_score": score,

            "reasons": reasons

        }



    def close(self):

        self.conn.close()



# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorSurvival()



    result = engine.analyze(
        creator
    )



    print()

    print(
        "========================================"
    )

    print(
        "CREATOR SURVIVAL"
    )

    print(
        "========================================"
    )



    if result is None:


        print(
            "Creator tidak ditemukan"
        )


    else:


        print(
            f"Creator          : {result['creator']}"
        )

        print(
            f"Total Token      : {result['total_token']}"
        )

        print(
            f"Survivor Token   : {result['survivor_token']}"
        )

        print(
            f"Dead Token       : {result['dead_token']}"
        )

        print(
            f"Success Rate     : {result['success_rate']}%"
        )

        print(
            f"Breakout Token   : {result['breakout_token']}"
        )

        print(
            f"Highest MC       : {result['highest_mc']:.2f}"
        )

        print("----------------------------------------")

        print(
            f"Survival Score   : {result['survival_score']}/100"
        )

        print("----------------------------------------")

        print(
            "REASONS"
        )


        for reason in result["reasons"]:

            print(
                "-",
                reason
            )



    engine.close()