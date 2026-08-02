import sqlite3



class CreatorReliability:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()



    # ======================================
    # Calculate Reliability
    # ======================================

    def calculate(self, creator):


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


        if not row:

            return None



        total_token = row[0] or 0
        highest_mc = row[1] or 0
        avg_mc = row[2] or 0



        score = 0



        # =========================
        # HISTORY SCORE
        # =========================

        if total_token >= 100:

            history = 30

        elif total_token >= 50:

            history = 25

        elif total_token >= 20:

            history = 20

        elif total_token >= 5:

            history = 10

        else:

            history = 3



        score += history



        # =========================
        # BREAKOUT SCORE
        # =========================

        if highest_mc >= 1000:

            breakout = 40

        elif highest_mc >= 500:

            breakout = 30

        elif highest_mc >= 100:

            breakout = 20

        elif highest_mc >= 50:

            breakout = 10

        else:

            breakout = 0



        score += breakout



        # =========================
        # CONSISTENCY SCORE
        # =========================


        if avg_mc >= 100:

            consistency = 30

        elif avg_mc >= 50:

            consistency = 20

        elif avg_mc >= 30:

            consistency = 10

        else:

            consistency = 0



        score += consistency



        return {

            "creator": creator,

            "total_token": total_token,

            "highest_mc": highest_mc,

            "avg_mc": avg_mc,

            "history_score": history,

            "breakout_score": breakout,

            "consistency_score": consistency,

            "reliability_score": min(score,100)

        }



    def close(self):

        self.conn.close()





# ======================================
# TEST MODE
# ======================================


if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    analyzer = CreatorReliability()


    result = analyzer.calculate(
        creator
    )



    print()

    print("==============================")
    print("CREATOR RELIABILITY")
    print("==============================")


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
            f"Highest MC       : {result['highest_mc']:.2f}"
        )

        print(
            f"Average MC       : {result['avg_mc']:.2f}"
        )


        print("--------------------------------")

        print(
            f"History Score    : {result['history_score']}/30"
        )

        print(
            f"Breakout Score   : {result['breakout_score']}/40"
        )

        print(
            f"Consistency      : {result['consistency_score']}/30"
        )


        print("--------------------------------")


        print(
            f"Reliability      : {result['reliability_score']}/100"
        )



    analyzer.close()