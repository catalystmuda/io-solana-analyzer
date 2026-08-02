import sqlite3
import json
import sys


DB = "backend/database/tokens.db"


class CreatorMemoryEngineV32:


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




    def maturity_score(self, total_tokens):

        if total_tokens >= 50:

            return 100


        elif total_tokens >= 20:

            return 80


        elif total_tokens >= 5:

            return 50


        else:

            return 30




    def confidence_level(self, maturity):

        if maturity >= 80:

            return "HIGH"


        elif maturity >= 50:

            return "MEDIUM"


        else:

            return "LOW"




    def analyze(self, creator):


        data = self.load_creator(creator)


        if not data:

            return {
                "found": False,
                "creator": creator
            }



        score = 0


        signals = list(data["signals"])



        score += data["reputation"]


        score -= data["risk"]



        if data["breakout_count"] > 0:

            score += 10

            signals.append(
                "Breakout history"
            )



        if data["survivor_count"] > 0:

            score += 10

            signals.append(
                "Survivor history"
            )



        if data["highest_mc"] >= 500:

            score += 10

            signals.append(
                "Strong market history"
            )



        raw_score = max(
            0,
            min(
                100,
                score
            )
        )



        maturity = self.maturity_score(
            data["total_tokens"]
        )


        confidence = self.confidence_level(
            maturity
        )



        adjusted_score = int(
            raw_score *
            (
                0.5 +
                maturity / 200
            )
        )



        if adjusted_score >= 80:

            decision = "ENTRY CANDIDATE"


        elif adjusted_score >= 50:

            decision = "WATCH LIST"


        else:

            decision = "AVOID"




        if maturity < 50 and raw_score >= 80:

            alpha_type = "EARLY ALPHA"


        elif maturity >= 80 and raw_score >= 80:

            alpha_type = "VETERAN SMART MONEY"


        else:

            alpha_type = "UNKNOWN"



        return {

            "creator": data["creator"],

            "found": True,

            "alpha_type": alpha_type,

            "raw_score": raw_score,

            "maturity": f"{maturity}%",

            "adjusted_score": adjusted_score,

            "decision": decision,

            "confidence": confidence,

            "sample_size": data["total_tokens"],

            "category": data["category"],

            "signals": list(dict.fromkeys(signals))

        }





if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Usage: python -m backend.analysis.creator_memory_engine_v32 CREATOR"
        )

        sys.exit()



    creator = sys.argv[1]


    engine = CreatorMemoryEngineV32()


    result = engine.analyze(creator)



    print("==============================")
    print(" CREATOR MEMORY ENGINE V32 ")
    print("==============================")


    for key,value in result.items():

        print(
            f"{key} : {value}"
        )