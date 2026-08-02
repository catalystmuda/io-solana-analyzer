import sqlite3



class CreatorPatternMemory:



    def __init__(self):


        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )


        self.cursor = self.conn.cursor()




    # =====================================
    # CREATOR PATTERN ANALYSIS
    # =====================================


    def analyze(self, creator):



        self.cursor.execute(
            """
            SELECT
                name,
                symbol,
                market_cap_sol
            FROM tokens
            WHERE creator = ?
            """,
            (creator,)
        )



        rows = self.cursor.fetchall()



        if not rows:

            return None




        total_token = len(rows)



        names = []

        symbols = []



        for row in rows:


            if row[0]:

                names.append(
                    row[0].lower()
                )


            if row[1]:

                symbols.append(
                    row[1].lower()
                )






        # =====================================
        # DUPLICATE CHECK
        # =====================================


        duplicate_name = (
            len(names)
            -
            len(set(names))
        )



        duplicate_symbol = (
            len(symbols)
            -
            len(set(symbols))
        )






        # =====================================
        # LAUNCH FREQUENCY
        # =====================================


        launch_score = 0



        if total_token >= 50:


            launch_score = 40



        elif total_token >= 20:


            launch_score = 25



        elif total_token >= 5:


            launch_score = 10



        else:


            launch_score = 0






        # =====================================
        # PATTERN RISK
        # =====================================


        risk = 0



        reasons = []




        if launch_score >= 25:


            risk += 30


            reasons.append(
                "High launch frequency"
            )




        if duplicate_name > 0:


            risk += 25


            reasons.append(
                "Duplicate token names"
            )




        if duplicate_symbol > 0:


            risk += 25


            reasons.append(
                "Duplicate token symbols"
            )





        if total_token <= 3:


            reasons.append(
                "Early creator pattern"
            )





        risk = min(
            risk,
            100
        )






        pattern_score = 100 - risk






        if not reasons:


            reasons.append(
                "Clean creator pattern"
            )






        return {



            "creator": creator,


            "total_token": total_token,


            "pattern_score": pattern_score,


            "pattern_risk": risk,


            "duplicate_name": duplicate_name,


            "duplicate_symbol": duplicate_symbol,


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



    engine = CreatorPatternMemory()



    result = engine.analyze(
        creator
    )



    print()


    print("==============================")

    print(" CREATOR PATTERN MEMORY ")

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
            f"Total Token      : {result['total_token']}"
        )


        print(
            f"Pattern Score    : {result['pattern_score']}/100"
        )


        print(
            f"Pattern Risk     : {result['pattern_risk']}/100"
        )


        print(
            f"Duplicate Name   : {result['duplicate_name']}"
        )


        print(
            f"Duplicate Symbol : {result['duplicate_symbol']}"
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