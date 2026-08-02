import sqlite3



class CreatorReliability:



    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()



    # =====================================
    # ANALYZE CREATOR RELIABILITY
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



        if row is None or row[0] == 0:

            return None



        total_token = row[0]

        highest_mc = row[1] or 0

        average_mc = row[2] or 0



        # ===============================
        # HISTORY SCORE
        # ===============================

        history_score = 0


        if total_token >= 50:

            history_score = 30

        elif total_token >= 10:

            history_score = 20

        else:

            history_score = 10



        # ===============================
        # BREAKOUT SCORE
        # ===============================

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



        breakout_score = 0


        if breakout >= 3:

            breakout_score = 40


        elif breakout >= 1:

            breakout_score = 25



        # ===============================
        # CONSISTENCY
        # ===============================

        consistency = 0


        if average_mc >= 100:

            consistency = 30


        elif average_mc >= 50:

            consistency = 20


        else:

            consistency = 10



        reliability_score = (

            history_score +

            breakout_score +

            consistency

        )



        reliability_score = min(
            reliability_score,
            100
        )



        reasons = []



        if breakout == 0:

            reasons.append(
                "Belum ada breakout token"
            )


        if average_mc < 100:

            reasons.append(
                "Average marketcap rendah"
            )


        if total_token < 5:

            reasons.append(
                "Limited creator history"
            )


        if not reasons:

            reasons.append(
                "Creator reliability positif"
            )



        return {


            "creator": creator,

            "total_token": total_token,

            "highest_mc": highest_mc,

            "average_mc": average_mc,

            "reliability_score":
            reliability_score,

            "reasons": reasons

        }




    def calculate(self, creator):

        return self.analyze(
            creator
        )



    def close(self):

        self.conn.close()





# =====================================
# TEST
# =====================================


if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorReliability()


    result = engine.analyze(
        creator
    )



    print()

    print("==============================")
    print(" CREATOR RELIABILITY ")
    print("==============================")


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
        f"Average MC       : {result['average_mc']:.2f}"
    )


    print("--------------------------------")


    print(
        f"Reliability      : {result['reliability_score']}/100"
    )


    print("--------------------------------")

    print("REASONS")


    for r in result["reasons"]:

        print(
            "-",
            r
        )



    engine.close()