import sqlite3
import json
import sys


DB = "backend/database/tokens.db"


class CreatorMemoryEngineV32_1:


    def __init__(self):

        self.conn = sqlite3.connect(DB)
        self.cur = self.conn.cursor()



    def load_creator(self, creator):

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
            (creator.strip(),)
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



    def calculate_maturity(self, total_tokens):

        if total_tokens >= 50:

            return 100


        elif total_tokens >= 20:

            return 80


        elif total_tokens >= 5:

            return 50


        else:

            return 30




    def confidence(self, maturity):

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



        # reputation

        score += data["reputation"]



        # risk penalty

        score -= data["risk"]



        # breakout history

        if data["breakout_count"] > 0:

            score += 10

            signals.append(
                "Breakout history"
            )



        # survivor

        if data["survivor_count"] > 0:

            score += 10

            signals.append(
                "Survivor history"
            )



        # market history

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



        maturity = self.calculate_maturity(
            data["total_tokens"]
        )



        conf = self.confidence(
            maturity
        )



        # early alpha bonus

        if maturity <= 30 and raw_score >= 80:

            signals.append(
                "Early alpha - limited history"
            )



        # decision berdasarkan kualitas

        if raw_score >= 80:

            decision = "ENTRY CANDIDATE"


        elif raw_score >= 50:

            decision = "WATCH LIST"


        else:

            decision = "AVOID"




        if raw_score >= 80 and maturity <= 30:

            alpha_type = "EARLY ALPHA"


        elif raw_score >= 80 and maturity >= 80:

            alpha_type = "VETERAN SMART MONEY"


        elif raw_score >= 50:

            alpha_type = "PROMISING CREATOR"


        else:

            alpha_type = "DANGEROUS CREATOR"




        return {

            "creator": data["creator"],

            "found": True,

            "alpha_type": alpha_type,

            "quality_score": raw_score,

            "maturity": f"{maturity}%",

            "confidence": conf,

            "decision": decision,

            "sample_size": data["total_tokens"],

            "category": data["category"],

            "highest_mc": data["highest_mc"],

            "signals": list(dict.fromkeys(signals))

        }





if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Usage: python -m backend.analysis.creator_memory_engine_v32_1 CREATOR"
        )

        sys.exit()



    creator = sys.argv[1]


    engine = CreatorMemoryEngineV32_1()


    result = engine.analyze(
        creator
    )


    print("==============================")
    print(" CREATOR MEMORY ENGINE V32.1 ")
    print("==============================")


    for k,v in result.items():

        print(
            f"{k} : {v}"
        )