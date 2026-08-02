import sqlite3



class CreatorRanking:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()



    # ======================================
    # TOP CREATOR
    # ======================================


    def top_creators(self, limit=10):


        self.cursor.execute(
            """
            SELECT

                ca.creator,
                ca.final_score,
                ca.verdict,
                ca.confidence,
                ca.survival_score,
                ca.behavior_risk,

                COUNT(t.id),
                MAX(t.market_cap_sol)

            FROM creator_analysis ca

            LEFT JOIN tokens t

            ON ca.creator = t.creator


            GROUP BY ca.creator


            ORDER BY ca.final_score DESC


            LIMIT ?

            """,
            (limit,)
        )


        return self.cursor.fetchall()




    # ======================================
    # RISK CREATOR
    # ======================================


    def risky_creators(self, limit=10):


        self.cursor.execute(
            """
            SELECT

                ca.creator,
                ca.final_score,
                ca.verdict,
                ca.behavior_risk,
                ca.survival_score,

                COUNT(t.id),
                MAX(t.market_cap_sol)


            FROM creator_analysis ca


            LEFT JOIN tokens t


            ON ca.creator = t.creator


            GROUP BY ca.creator


            ORDER BY ca.final_score ASC


            LIMIT ?

            """,
            (limit,)
        )


        return self.cursor.fetchall()




    def close(self):

        self.conn.close()





if __name__ == "__main__":


    engine = CreatorRanking()



    print()

    print("==============================")
    print("TOP CREATOR ALPHA")
    print("==============================")


    for i, row in enumerate(
        engine.top_creators(),
        1
    ):


        print()

        print(
            f"#{i}"
        )


        print(
            "Creator      :",
            row[0]
        )


        print(
            "Score        :",
            row[1]
        )


        print(
            "Verdict      :",
            row[2]
        )


        print(
            "Confidence   :",
            row[3]
        )


        print(
            "Survival     :",
            row[4]
        )


        print(
            "Risk         :",
            row[5]
        )


        print(
            "Total Token  :",
            row[6]
        )


        print(
            "Highest MC   :",
            row[7]
        )




    print()

    print("==============================")
    print("RISKY CREATOR")
    print("==============================")


    for i, row in enumerate(
        engine.risky_creators(),
        1
    ):


        print()

        print(
            f"#{i}"
        )


        print(
            "Creator      :",
            row[0]
        )


        print(
            "Score        :",
            row[1]
        )


        print(
            "Verdict      :",
            row[2]
        )


        print(
            "Risk         :",
            row[3]
        )


        print(
            "Survival     :",
            row[4]
        )


        print(
            "Total Token  :",
            row[5]
        )


        print(
            "Highest MC   :",
            row[6]
        )



    engine.close()