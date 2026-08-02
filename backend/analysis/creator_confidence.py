import sqlite3



class CreatorConfidence:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()



    # =====================================
    # CREATOR CONFIDENCE ANALYSIS
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



        total_token = row[0] or 0

        highest_mc = row[1] or 0

        avg_mc = row[2] or 0



        # =====================================
        # HISTORY SCORE
        # =====================================

        history_score = 0



        if total_token >= 100:

            history_score += 50

        elif total_token >= 50:

            history_score += 40

        elif total_token >= 20:

            history_score += 30

        elif total_token >= 10:

            history_score += 20

        else:

            history_score += 10




        # =====================================
        # PERFORMANCE SCORE
        # =====================================

        performance_score = 0



        if highest_mc >= 1000:

            performance_score += 30

        elif highest_mc >= 500:

            performance_score += 25

        elif highest_mc >= 100:

            performance_score += 15

        else:

            performance_score += 5




        # =====================================
        # CONSISTENCY SCORE
        # =====================================

        consistency_score = 0



        if avg_mc >= 100:

            consistency_score += 20

        elif avg_mc >= 50:

            consistency_score += 15

        elif avg_mc >= 20:

            consistency_score += 10

        else:

            consistency_score += 5




        confidence_score = (

            history_score +

            performance_score +

            consistency_score

        )



        confidence_score = min(
            confidence_score,
            100
        )




        # =====================================
        # LABEL
        # =====================================


        if confidence_score >= 75:

            confidence = "HIGH"


        elif confidence_score >= 50:

            confidence = "MEDIUM"


        else:

            confidence = "LOW"




        # =====================================
        # WEIGHT
        # =====================================


        if confidence == "HIGH":

            weight = 1.0


        elif confidence == "MEDIUM":

            weight = 0.75


        else:

            weight = 0.5




        return {


            "creator": creator,

            "total_token": total_token,

            "highest_mc": highest_mc,

            "avg_mc": avg_mc,

            "history_score": history_score,

            "performance_score": performance_score,

            "consistency_score": consistency_score,

            "confidence_score": confidence_score,

            "confidence": confidence,

            "weight": weight

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



    engine = CreatorConfidence()



    result = engine.analyze(
        creator
    )



    print()

    print("==============================")
    print(" CREATOR CONFIDENCE ")
    print("==============================")



    if result is None:


        print(
            "Creator tidak ditemukan"
        )


    else:


        print(
            f"Creator             : {result['creator']}"
        )


        print(
            f"Total Token         : {result['total_token']}"
        )


        print(
            f"Highest MC          : {result['highest_mc']:.2f}"
        )


        print(
            f"Average MC          : {result['avg_mc']:.2f}"
        )


        print("--------------------------------")


        print(
            f"Confidence Score    : {result['confidence_score']}/100"
        )


        print(
            f"Confidence          : {result['confidence']}"
        )


        print(
            f"Weight              : {result['weight']}"
        )


    engine.close()