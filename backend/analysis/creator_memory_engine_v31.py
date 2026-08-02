import sqlite3
import json
import sys


DB = "backend/database/tokens.db"


class CreatorMemoryEngineV31:


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




    def confidence_weight(self, total_tokens):

        if total_tokens >= 50:

            return 1.0


        elif total_tokens >= 20:

            return 0.8


        elif total_tokens >= 5:

            return 0.5


        else:

            return 0.3




    def analyze(self, creator):


        data = self.load_creator(creator)


        if not data:

            return {

                "found": False,
                "creator": creator

            }



        raw_score = 0


        signals = list(data["signals"])



        raw_score += data["reputation"]


        raw_score -= data["risk"]



        if data["breakout_count"] > 0:

            raw_score += 10

            signals.append(
                "Breakout history"
            )



        if data["survivor_count"] > 0:

            raw_score += 10

            signals.append(
                "Survivor history"
            )



        if data["highest_mc"] >= 500:

            raw_score += 10

            signals.append(
                "Strong market history"
            )



        raw_score = max(
            0,
            min(
                100,
                raw_score
            )
        )



        weight = self.confidence_weight(
            data["total_tokens"]
        )


        adjusted_score = int(
            raw_score * weight
            +
            raw_score * 0.5
        )



        adjusted_score = min(
            100,
            adjusted_score
        )



        if data["total_tokens"] >= 20:

            confidence = "HIGH"


        elif data["total_tokens"] >= 5:

            confidence = "MEDIUM"


        else:

            confidence = "LOW"




        if adjusted_score >= 80:

            decision = "ENTRY CANDIDATE"


        elif adjusted_score >= 50:

            decision = "WATCH LIST"


        else:

            decision = "AVOID"




        if raw_score >= 80:

            dna = "SMART MONEY CREATOR"

        elif raw_score >= 50:

            dna = "PROMISING CREATOR"

        else:

            dna = "DANGEROUS CREATOR"




        return {

            "creator": data["creator"],

            "found": True,

            "dna": dna,

            "raw_score": raw_score,

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
            "Usage: python -m backend.analysis.creator_memory_engine_v31 CREATOR"
        )

        sys.exit()



    creator = sys.argv[1]


    engine = CreatorMemoryEngineV31()


    result = engine.analyze(creator)



    print("==============================")
    print(" CREATOR MEMORY ENGINE V31 ")
    print("==============================")


    for key,value in result.items():

        print(
            f"{key} : {value}"
        )