import sqlite3



class CreatorAlphaScore:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()



    # ==========================================
    # CREATOR ALPHA SCORE
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
        # SURVIVAL
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


        survivor = self.cursor.fetchone()[0]



        survival_ratio = 0


        if total_token > 0:

            survival_ratio = (
                survivor / total_token
            ) * 100




        # ======================================
        # BREAKOUT
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


        breakout = self.cursor.fetchone()[0]



        # ======================================
        # ALPHA SCORE
        #
        # Survival       30
        # Breakout       25
        # Market Quality 20
        # History        15
        # Activity       10
        #
        # ======================================


        score = 0



        # Survival

        if survival_ratio >= 50:

            score += 30

        elif survival_ratio >= 20:

            score += 20

        elif survival_ratio > 0:

            score += 10





        # Breakout


        if breakout >= 3:

            score += 25

        elif breakout >= 1:

            score += 15





        # Market quality


        if highest_mc >= 1000:

            score += 20

        elif highest_mc >= 500:

            score += 15

        elif highest_mc >= 100:

            score += 10





        # History


        if total_token >= 50:

            score += 15

        elif total_token >= 10:

            score += 10

        else:

            score += 5





        # Activity


        if avg_mc >= 100:

            score += 10

        elif avg_mc >= 50:

            score += 5





        score = min(score,100)





        # ======================================
        # GRADE
        # ======================================


        if score >= 80:

            grade = "A"

            status = "EARLY ALPHA CREATOR"


        elif score >= 60:

            grade = "B"

            status = "PROMISING CREATOR"


        elif score >= 40:

            grade = "C"

            status = "WATCH LIST"


        else:

            grade = "D"

            status = "AVOID CREATOR"





        reasons = []



        if survivor > 0:

            reasons.append(
                "Survival token detected"
            )


        if breakout > 0:

            reasons.append(
                "Breakout token detected"
            )


        if highest_mc >= 500:

            reasons.append(
                "Strong marketcap history"
            )


        if total_token < 5:

            reasons.append(
                "Limited creator history"
            )


        if score < 40:

            reasons.append(
                "Tidak ada bukti alpha"
            )





        return {


            "creator": creator,

            "alpha_score": score,

            "grade": grade,

            "status": status,

            "total_token": total_token,

            "highest_mc": highest_mc,

            "avg_mc": avg_mc,

            "survival": survivor,

            "breakout": breakout,

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



    engine = CreatorAlphaScore()



    result = engine.analyze(
        creator
    )



    print()


    print("==============================")
    print(" CREATOR ALPHA SCORE ")
    print("==============================")



    if result is None:

        print(
            "Creator tidak ditemukan"
        )


    else:


        print(
            f"Creator       : {result['creator']}"
        )


        print("--------------------------------")


        print(
            f"Alpha Score   : {result['alpha_score']}/100"
        )


        print(
            f"Grade         : {result['grade']}"
        )


        print(
            f"Status        : {result['status']}"
        )


        print("--------------------------------")


        print(
            f"Total Token   : {result['total_token']}"
        )


        print(
            f"Highest MC    : {result['highest_mc']:.2f}"
        )


        print(
            f"Average MC    : {result['avg_mc']:.2f}"
        )


        print(
            f"Survivor      : {result['survival']}"
        )


        print(
            f"Breakout      : {result['breakout']}"
        )


        print("--------------------------------")


        print(
            "SIGNALS"
        )


        for r in result["reasons"]:

            print(
                "-",
                r
            )



    engine.close()