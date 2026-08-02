import sqlite3
import json
import sys


DB = "backend/database/tokens.db"


class CreatorMemoryEngineV30:


    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.cur = self.conn.cursor()



    def load_creator(self, creator):

        creator = creator.strip()


        self.cur.execute(
            """
            SELECT
            creator,
            total_tokens,
            highest_mc,
            average_mc,
            breakout_count,
            survivor_count,
            reputation_score,
            risk_score,
            category,
            signals
            FROM creator_memory
            WHERE LOWER(TRIM(creator)) = LOWER(TRIM(?))
            """,
            (creator,)
        )


        row = self.cur.fetchone()


        if not row:

            # fallback search
            self.cur.execute(
                """
                SELECT
                creator,
                total_tokens,
                highest_mc,
                average_mc,
                breakout_count,
                survivor_count,
                reputation_score,
                risk_score,
                category,
                signals
                FROM creator_memory
                WHERE creator LIKE ?
                """,
                (creator[:20] + "%",)
            )


            row = self.cur.fetchone()



        if not row:

            return None



        try:

            signals = json.loads(row[9]) if row[9] else []

        except:

            signals = []



        return {

            "creator": row[0],
            "total_tokens": row[1],
            "highest_mc": row[2],
            "average_mc": row[3],
            "breakout_count": row[4],
            "survivor_count": row[5],
            "reputation": row[6],
            "risk": row[7],
            "category": row[8],
            "signals": signals

        }



    def analyze(self, creator):


        data = self.load_creator(creator)



        if not data:

            return {

                "found": False,
                "creator": creator

            }



        score = 0


        signals = list(data["signals"])



        # base reputation

        score += data["reputation"]



        # risk penalty

        score -= data["risk"]




        # breakout history

        if data["breakout_count"] > 0:

            score += 10

            signals.append(
                "Multiple breakout history"
            )




        # survivor history

        if data["survivor_count"] > 0:

            score += 10

            signals.append(
                "High survival ratio"
            )




        # market history

        if data["highest_mc"] >= 500:

            score += 10

            signals.append(
                "Strong market history"
            )




        score = max(
            0,
            min(
                100,
                score
            )
        )




        if score >= 80:

            dna = "SMART MONEY CREATOR"
            decision = "ENTRY CANDIDATE"


        elif score >= 50:

            dna = "PROMISING CREATOR"
            decision = "WATCH LIST"


        else:

            dna = "DANGEROUS CREATOR"
            decision = "AVOID"




        return {

            "creator": data["creator"],

            "found": True,

            "dna": dna,

            "score": score,

            "decision": decision,

            "category": data["category"],

            "total_tokens": data["total_tokens"],

            "highest_mc": data["highest_mc"],

            "signals": list(dict.fromkeys(signals))

        }





if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Usage:"
        )

        print(
            "python -m backend.analysis.creator_memory_engine_v30 CREATOR"
        )

        sys.exit()



    creator = sys.argv[1]


    engine = CreatorMemoryEngineV30()


    result = engine.analyze(creator)



    print("==============================")
    print(" CREATOR MEMORY ENGINE V30.1 ")
    print("==============================")


    for key,value in result.items():

        print(
            f"{key} : {value}"
        )