import sqlite3


DB = "backend/database/tokens.db"


class CreatorMemoryEngine:


    def __init__(self):
        self.conn = sqlite3.connect(DB)


    def get_creator_memory(self, creator):

        cur = self.conn.cursor()

        cur.execute(
            """
            SELECT
            reputation_score,
            risk_score,
            category,
            signals
            FROM creator_memory
            WHERE creator=?
            """,
            (creator,)
        )

        row = cur.fetchone()

        if not row:
            return {
                "found":False,
                "score":0,
                "category":"UNKNOWN"
            }


        reputation = row[0]
        risk = row[1]
        category = row[2]
        signals = row[3]


        score = reputation - risk


        if score >=80:
            decision="ENTRY CANDIDATE"

        elif score >=50:
            decision="WATCH LIST"

        else:
            decision="AVOID"



        return {

            "found":True,
            "score":score,
            "decision":decision,
            "category":category,
            "signals":signals

        }



if __name__=="__main__":


    import sys


    creator=sys.argv[1]


    engine=CreatorMemoryEngine()

    result=engine.get_creator_memory(
        creator
    )


    print("==============================")
    print(" CREATOR MEMORY ENGINE V29 ")
    print("==============================")

    print("creator :",creator)

    for k,v in result.items():
        print(k,":",v)