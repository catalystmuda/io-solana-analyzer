import sqlite3


class CreatorNetwork:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()



    # =====================================
    # ANALYZE CREATOR NETWORK
    # =====================================

    def analyze(self, creator):


        self.cursor.execute(
            """
            SELECT
                creator,
                COUNT(*)
            FROM tokens
            GROUP BY creator
            """
        )


        creators = self.cursor.fetchall()


        total_creator = len(creators)



        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM tokens
            WHERE creator = ?
            """,
            (creator,)
        )


        own_tokens = self.cursor.fetchone()[0]



        # =================================
        # NETWORK SCORE
        # =================================


        score = 50


        reasons = []



        # creator dengan banyak token

        if own_tokens >= 30:

            score -= 20

            reasons.append(
                "Creator melakukan banyak launch"
            )


        elif own_tokens >= 10:

            score -= 10

            reasons.append(
                "Creator memiliki banyak token"
            )



        # jumlah creator database


        if total_creator > 1000:

            score += 10

            reasons.append(
                "Database creator cukup luas"
            )



        score = max(
            0,
            min(score,100)
        )



        return {


            "creator": creator,


            "total_creator": total_creator,


            "own_tokens": own_tokens,


            "network_score": score,


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


    engine = CreatorNetwork()


    result = engine.analyze(
        creator
    )



    print()

    print("==============================")
    print(" CREATOR NETWORK ")
    print("==============================")


    print(
        f"Creator        : {result['creator']}"
    )

    print(
        f"Total Creator  : {result['total_creator']}"
    )

    print(
        f"Token Created  : {result['own_tokens']}"
    )


    print("--------------------------------")


    print(
        f"Network Score  : {result['network_score']}/100"
    )


    print("--------------------------------")

    print("REASONS")


    for r in result["reasons"]:

        print(
            "-",
            r
        )


    engine.close()