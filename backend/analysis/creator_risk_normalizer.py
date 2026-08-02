import sqlite3



class CreatorRiskNormalizer:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()



    # ==========================================
    # CREATOR RISK NORMALIZER
    # ==========================================


    def analyze(self, creator):


        risk = 0

        reasons = []



        # ======================================
        # BASIC TOKEN DATA
        # ======================================


        self.cursor.execute(
            """
            SELECT
                COUNT(*),
                AVG(market_cap_sol),
                MAX(market_cap_sol)
            FROM tokens
            WHERE creator = ?
            """,
            (creator,)
        )


        row = self.cursor.fetchone()



        if row is None or row[0] == 0:

            return None



        total_token = row[0] or 0

        avg_mc = row[1] or 0

        highest_mc = row[2] or 0





        # ======================================
        # MASS LAUNCH RISK
        # ======================================


        if total_token >= 50:

            risk += 30

            reasons.append(
                "Mass launch detected"
            )


        elif total_token >= 20:

            risk += 20

            reasons.append(
                "High launch frequency"
            )


        elif total_token >= 10:

            risk += 10





        # ======================================
        # MARKETCAP QUALITY
        # ======================================


        if highest_mc < 100:

            risk += 25

            reasons.append(
                "Tidak ada marketcap kuat"
            )


        elif highest_mc < 500:

            risk += 10





        # ======================================
        # SURVIVAL CHECK
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



        if survivor == 0:

            risk += 20

            reasons.append(
                "Tidak ada token survivor"
            )





        # ======================================
        # BREAKOUT CHECK
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



        if breakout == 0:

            risk += 10

            reasons.append(
                "Tidak ada breakout token"
            )





        # ======================================
        # DUPLICATE PATTERN
        # ======================================


        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM
            (
                SELECT name
                FROM tokens
                WHERE creator = ?
                GROUP BY name
                HAVING COUNT(*) > 1
            )
            """,
            (creator,)
        )


        duplicate_name = self.cursor.fetchone()[0]



        if duplicate_name > 0:

            risk += 5

            reasons.append(
                "Duplicate token names"
            )





        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM
            (
                SELECT symbol
                FROM tokens
                WHERE creator = ?
                GROUP BY symbol
                HAVING COUNT(*) > 1
            )
            """,
            (creator,)
        )


        duplicate_symbol = self.cursor.fetchone()[0]



        if duplicate_symbol > 0:

            risk += 5

            reasons.append(
                "Duplicate token symbols"
            )





        # ======================================
        # FINAL LIMIT
        # ======================================


        risk = min(
            risk,
            100
        )





        # ======================================
        # RISK LEVEL
        # ======================================


        if risk >= 80:

            level = "VERY HIGH RISK"


        elif risk >= 60:

            level = "HIGH RISK"


        elif risk >= 40:

            level = "MEDIUM RISK"


        else:

            level = "LOW RISK"





        if not reasons:

            reasons.append(
                "Creator pattern sehat"
            )





        return {


            "creator": creator,


            "risk_score": risk,


            "risk_level": level,


            "total_token": total_token,


            "avg_mc": avg_mc,


            "highest_mc": highest_mc,


            "survivor": survivor,


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



    engine = CreatorRiskNormalizer()



    result = engine.analyze(
        creator
    )



    print()


    print("==============================")
    print(" CREATOR RISK NORMALIZER ")
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
            f"Risk Score    : {result['risk_score']}/100"
        )


        print(
            f"Risk Level    : {result['risk_level']}"
        )


        print("--------------------------------")


        print(
            f"Total Token   : {result['total_token']}"
        )


        print(
            f"Average MC    : {result['avg_mc']:.2f}"
        )


        print(
            f"Highest MC    : {result['highest_mc']:.2f}"
        )


        print(
            f"Survivor      : {result['survivor']}"
        )


        print(
            f"Breakout      : {result['breakout']}"
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