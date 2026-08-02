import sqlite3
import json


DB = "backend/database/tokens.db"


class CreatorMemoryV26:

    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.cur = self.conn.cursor()


    def load_creators(self):

        rows = self.cur.execute("""
            SELECT
                creator,
                market_cap_sol,
                name,
                symbol
            FROM tokens
            WHERE creator IS NOT NULL
        """).fetchall()


        creators = {}

        for creator, mc, name, symbol in rows:

            if creator not in creators:
                creators[creator] = []

            creators[creator].append({
                "mc": mc or 0,
                "name": name,
                "symbol": symbol
            })


        return creators



    def analyze(self, creator, tokens):

        total = len(tokens)

        highest = max(
            x["mc"] for x in tokens
        )

        average = sum(
            x["mc"] for x in tokens
        ) / total


        breakout = sum(
            1 for x in tokens
            if x["mc"] >= 500
        )


        survivor = sum(
            1 for x in tokens
            if x["mc"] >= 100
        )


        success_rate = int(
            (breakout / total) * 100
        )


        score = 0


        # market strength

        if highest >= 500:
            score += 40

        elif highest >= 100:
            score += 20


        # success

        score += int(
            success_rate * 0.35
        )


        # survivor

        if survivor:
            score += 15


        # early creator bonus

        if total <= 3:
            score += 10


        score = min(
            100,
            score
        )



        # risk

        risk = 0


        if total > 30:
            risk += 30


        if average < 50:
            risk += 30


        if breakout == 0:
            risk += 25


        risk = min(
            100,
            risk
        )



        if score >= 85:

            category = "SMART MONEY CREATOR"

        elif score >= 60:

            category = "PROMISING CREATOR"

        elif score >= 40:

            category = "WATCH CREATOR"

        else:

            category = "LOW QUALITY CREATOR"



        if total <=2:

            confidence = "LOW"

        elif total <=10:

            confidence = "MEDIUM"

        else:

            confidence = "HIGH"



        signals=[]


        if breakout:
            signals.append(
                "Previous breakout"
            )


        if survivor:
            signals.append(
                "Survivor token"
            )


        if success_rate >=50:
            signals.append(
                "High success ratio"
            )


        if total <=3:
            signals.append(
                "Early creator"
            )


        return {

            "creator":creator,
            "total":total,
            "highest":highest,
            "average":average,
            "breakout":breakout,
            "survivor":survivor,
            "success_rate":success_rate,
            "score":score,
            "risk":risk,
            "category":category,
            "confidence":confidence,
            "signals":signals
        }



    def save(self,data):

        self.cur.execute("""
        INSERT OR REPLACE INTO creator_memory

        (
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
        )

        VALUES (?,?,?,?,?,?,?,?,?,?)

        """,

        (
        data["creator"],
        data["total"],
        data["highest"],
        data["average"],
        data["breakout"],
        data["survivor"],
        data["score"],
        data["risk"],
        data["category"],
        json.dumps(
            data["signals"]
        )
        ))



    def run(self):

        creators = self.load_creators()


        results=[]


        for creator,tokens in creators.items():

            result=self.analyze(
                creator,
                tokens
            )

            self.save(result)

            results.append(result)



        self.conn.commit()



        results.sort(
            key=lambda x:x["score"],
            reverse=True
        )


        print("==============================")
        print(" CREATOR MEMORY V26 ")
        print("==============================")

        print(
            "Creators Updated :",
            len(results)
        )


        print("\nTOP MEMORY")


        for i,r in enumerate(results[:10],1):

            print()
            print("#",i)
            print(
                "Creator :",
                r["creator"]
            )
            print(
                "Score   :",
                r["score"]
            )
            print(
                "Class   :",
                r["category"]
            )
            print(
                "Success :",
                str(r["success_rate"])+"%"
            )
            print(
                "Confidence :",
                r["confidence"]
            )
            print(
                "Signals :",
                r["signals"]
            )



if __name__=="__main__":

    engine=CreatorMemoryV26()

    engine.run()