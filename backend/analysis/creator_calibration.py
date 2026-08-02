import sqlite3




class CreatorCalibration:



    def __init__(self):


        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )


        self.cursor = self.conn.cursor()




    # =====================================
    # CALIBRATE CREATOR
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




        # =================================
        # TOKEN HISTORY SCORE
        # =================================


        history_score = 0



        if total_token >= 50:

            history_score = 20


        elif total_token >= 10:

            history_score = 15


        elif total_token >= 3:

            history_score = 10


        else:

            history_score = 5





        # =================================
        # MARKET QUALITY SCORE
        # =================================


        market_score = 0



        if highest_mc >= 1000:

            market_score = 30


        elif highest_mc >= 500:

            market_score = 25


        elif highest_mc >= 100:

            market_score = 15


        else:

            market_score = 5





        # =================================
        # CONSISTENCY SCORE
        # =================================


        consistency_score = 0



        if average_mc >= 500:

            consistency_score = 30


        elif average_mc >= 100:

            consistency_score = 20


        elif average_mc >= 50:

            consistency_score = 10


        else:

            consistency_score = 5





        # =================================
        # LOW SAMPLE PENALTY
        # =================================


        penalty = 0



        if total_token == 1:


            penalty = 10



        elif total_token < 3:


            penalty = 5





        final_score = (

            history_score

            +

            market_score

            +

            consistency_score

            -

            penalty

        )



        final_score = max(
            0,
            min(
                final_score,
                100
            )
        )




        reasons = []



        if total_token == 1:


            reasons.append(
                "Limited creator history"
            )



        if highest_mc >= 500:


            reasons.append(
                "Strong marketcap signal"
            )



        if average_mc < 50:


            reasons.append(
                "Low average marketcap"
            )



        if total_token >= 30:


            reasons.append(
                "Large token production"
            )



        if not reasons:


            reasons.append(
                "Balanced creator profile"
            )




        return {


            "creator": creator,


            "calibration_score": final_score,


            "total_token": total_token,


            "highest_mc": highest_mc,


            "average_mc": average_mc,


            "history_score": history_score,


            "market_score": market_score,


            "consistency_score": consistency_score,


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



    engine = CreatorCalibration()



    result = engine.analyze(
        creator
    )



    print()


    print("==============================")

    print(" CREATOR CALIBRATION ")

    print("==============================")



    if result is None:


        print(
            "Creator tidak ditemukan"
        )


    else:


        print(
            f"Creator            : {result['creator']}"
        )


        print("--------------------------------")


        print(
            f"Calibration Score  : {result['calibration_score']}/100"
        )


        print(
            f"Total Token        : {result['total_token']}"
        )


        print(
            f"Highest MC         : {result['highest_mc']:.2f}"
        )


        print(
            f"Average MC         : {result['average_mc']:.2f}"
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