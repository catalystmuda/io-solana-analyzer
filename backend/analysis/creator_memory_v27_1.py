import sqlite3
import json


DB = "backend/database/tokens.db"


class CreatorMemoryV271:

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
            t["mc"] for t in tokens
        )


        average = sum(
            t["mc"] for t in tokens
        ) / total


        breakout = sum(
            1 for t in tokens
            if t["mc"] >= 500
        )


        survivor = sum(
            1 for t in tokens
            if t["mc"] >= 100
        )


        success_rate = int(
            breakout / total * 100
        )


        # MARKET QUALITY V27.1

        market = 0


        if highest >= 500:
            market += 40

        elif highest >= 100:
            market += 15


        if breakout > 0:
            market += 30


        if survivor > 0:
            market += 10


        if average >= 100:
            market += 10


        market = min(
            100,
            market
        )



        # BREAKOUT CALIBRATION

        reputation = 0


        reputation += int(
            market * 0.45
        )


        reputation += int(
            success_rate * 0.45
        )


        if total <= 3:
            reputation += 10


        reputation = min(
            100,
            reputation
        )



        # RISK

        risk = 0


        if total >= 20:
            risk += 25


        if success_rate == 0:
            risk += 40


        if average < 50:
            risk += 20


        risk = min(
            100,
            risk
        )



        if reputation >= 90:
            grade = "A+"

        elif reputation >= 75:
            grade = "A"

        elif reputation >= 60:
            grade = "B"

        elif reputation >= 40:
            grade = "C"

        else:
            grade = "D"



        if total == 1:
            confidence = "LOW"

        elif total < 10:
            confidence = "MEDIUM"

        else:
            confidence = "HIGH"



        signals=[]


        if breakout:
            signals.append(
                "Real breakout history"
            )


        if success_rate >=50:
            signals.append(
                "High creator success"
            )


        if total <=3:
            signals.append(
                "Early creator"
            )


        if risk >=50:
            signals.append(
                "Risk adjusted"
            )


        return {

            "creator":creator,
            "total":total,
            "highest":highest,
            "average":average,
            "breakout":breakout,
            "survivor":survivor,
            "success_rate":success_rate,
            "market":market,
            "reputation":reputation,
            "risk":risk,
            "grade":grade,
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
            data["reputation"],
            data["risk"],
            data["grade"],
            json.dumps(data["signals"])
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
            key=lambda x:x["reputation"],
            reverse=True
        )


        print("==============================")
        print(" CREATOR MEMORY V27.1 ")
        print("==============================")

        print(
            "Creators Updated :",
            len(results)
        )


        print("\nTOP CALIBRATION")


        for i,r in enumerate(results[:10],1):

            print()
            print("#",i)
            print(
                "Creator :",
                r["creator"]
            )
            print(
                "Grade   :",
                r["grade"]
            )
            print(
                "Rep     :",
                r["reputation"]
            )
            print(
                "Risk    :",
                r["risk"]
            )
            print(
                "Market  :",
                r["market"]
            )
            print(
                "Success :",
                str(r["success_rate"])+"%"
            )
            print(
                "Signals :",
                r["signals"]
            )



if __name__=="__main__":

    CreatorMemoryV271().run()