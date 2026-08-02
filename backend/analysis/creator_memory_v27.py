import sqlite3
import json


DB = "backend/database/tokens.db"


class CreatorMemoryV27:

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
            breakout / total * 100
        )


        # MARKET QUALITY

        market_quality = 0


        if highest >= 500:
            market_quality += 50

        elif highest >= 100:
            market_quality += 25


        if average >= 100:
            market_quality += 30


        if survivor:
            market_quality += 20


        market_quality = min(
            100,
            market_quality
        )



        # REPUTATION

        reputation = 0


        reputation += int(
            market_quality * 0.5
        )


        reputation += int(
            success_rate * 0.35
        )


        if total <=3:
            reputation += 15


        reputation = min(
            100,
            reputation
        )



        # GRADE

        if reputation >=95:
            grade="A+"

        elif reputation >=80:
            grade="A"

        elif reputation >=60:
            grade="B"

        elif reputation >=40:
            grade="C"

        else:
            grade="D"



        # CONFIDENCE

        if total == 1:
            confidence="LOW"

        elif total <10:
            confidence="MEDIUM"

        else:
            confidence="HIGH"



        signals=[]


        if breakout:
            signals.append(
                "Breakout history"
            )


        if market_quality >=50:
            signals.append(
                "Strong market quality"
            )


        if total <=3:
            signals.append(
                "Early creator"
            )


        if success_rate >=50:
            signals.append(
                "High success ratio"
            )


        return {

            "creator":creator,
            "total":total,
            "highest":highest,
            "average":average,
            "breakout":breakout,
            "survivor":survivor,
            "success_rate":success_rate,
            "market_quality":market_quality,
            "reputation":reputation,
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
        100-data["reputation"],
        data["grade"],
        json.dumps(data["signals"])
        ))



    def run(self):

        creators=self.load_creators()


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
        print(" CREATOR MEMORY V27 ")
        print("==============================")

        print(
            "Creators Updated :",
            len(results)
        )


        print("\nTOP REPUTATION")


        for i,r in enumerate(results[:10],1):

            print()
            print("#",i)
            print("Creator :",r["creator"])
            print("Grade   :",r["grade"])
            print("Rep     :",r["reputation"])
            print("Market  :",r["market_quality"])
            print("Success :",str(r["success_rate"])+"%")
            print("Conf    :",r["confidence"])
            print("Signals :",r["signals"])



if __name__=="__main__":

    engine=CreatorMemoryV27()

    engine.run()