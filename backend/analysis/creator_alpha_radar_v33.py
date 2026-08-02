import sqlite3
import json


DB = "backend/database/tokens.db"



class CreatorAlphaRadarV33:


    def __init__(self):

        self.conn = sqlite3.connect(DB)
        self.cur = self.conn.cursor()



    def load_all_creators(self):

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
            """
        )


        rows = self.cur.fetchall()


        creators = []


        for row in rows:


            try:

                signals = json.loads(row[9]) if row[9] else []

            except:

                signals = []



            creators.append({

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

            })


        return creators




    def maturity(self, tokens):

        if tokens >= 50:

            return 100

        elif tokens >= 20:

            return 80

        elif tokens >= 5:

            return 50

        else:

            return 30




    def analyze_creator(self, data):


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



        score = max(
            0,
            min(
                100,
                score
            )
        )



        maturity = self.maturity(
            data["total_tokens"]
        )



        if score >= 80 and maturity <= 30:

            alpha_type = "EARLY ALPHA"


        elif score >= 80 and maturity >= 80:

            alpha_type = "VETERAN SMART MONEY"


        elif score >= 50:

            alpha_type = "WATCH"


        else:

            alpha_type = "DANGEROUS"




        if maturity >= 80:

            confidence = "HIGH"

        elif maturity >= 50:

            confidence = "MEDIUM"

        else:

            confidence = "LOW"




        return {

            "creator": data["creator"],

            "quality": score,

            "type": alpha_type,

            "confidence": confidence,

            "maturity": maturity,

            "mc": data["highest_mc"],

            "signals": list(dict.fromkeys(signals))

        }




    def radar(self, limit=20):


        creators = self.load_all_creators()


        results = []


        for creator in creators:

            results.append(
                self.analyze_creator(creator)
            )



        results.sort(
            key=lambda x: x["quality"],
            reverse=True
        )



        return results[:limit]




if __name__ == "__main__":


    engine = CreatorAlphaRadarV33()


    results = engine.radar(20)



    print("==============================")
    print(" CREATOR ALPHA RADAR V33 ")
    print("==============================")

    print()

    print(
        "TOTAL SCANNED :",
        len(engine.load_all_creators())
    )


    print()


    for i,item in enumerate(results,1):


        print(
            f"#{i}"
        )

        print(
            "Creator :",
            item["creator"]
        )

        print(
            "Quality :",
            item["quality"]
        )

        print(
            "Type    :",
            item["type"]
        )

        print(
            "Confidence :",
            item["confidence"]
        )

        print(
            "Maturity :",
            str(item["maturity"]) + "%"
        )

        print(
            "Highest MC :",
            item["mc"]
        )

        print(
            "Signals :",
            item["signals"]
        )

        print(
            "------------------------------"
        )