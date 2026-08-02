import sqlite3
import json


DB = "backend/database/tokens.db"


class CreatorMemoryV25:

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



    def calculate(self, creator, tokens):

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


        # reputation

        score = 0


        if highest >= 500:
            score += 40


        if breakout > 0:
            score += 25


        if survivor > 0:
            score += 20


        if total <= 3:
            score += 10


        score = min(
            100,
            score
        )


        risk = 0


        if total > 30:
            risk += 40


        if average < 100:
            risk += 30


        if breakout == 0:
            risk += 20


        risk = min(
            100,
            risk
        )


        if score >= 80:

            category = "SMART MONEY CREATOR"

        elif score >= 50:

            category = "WATCH CREATOR"

        else:

            category = "LOW QUALITY CREATOR"



        signals=[]


        if breakout:
            signals.append(
                "Previous breakout"
            )


        if highest >= 500:
            signals.append(
                "Strong marketcap"
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
            "score":score,
            "risk":risk,
            "category":category,
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

        """,(
            data["creator"],
            data["total"],
            data["highest"],
            data["average"],
            data["breakout"],
            data["survivor"],
            data["score"],
            data["risk"],
            data["category"],
            json.dumps(data["signals"])
        ))



    def run(self):

        creators=self.load_creators()


        for creator,tokens in creators.items():

            result=self.calculate(
                creator,
                tokens
            )

            self.save(result)


        self.conn.commit()


        print("==============================")
        print(" CREATOR MEMORY V25 ")
        print("==============================")
        print(
            "Creators Saved :",
            len(creators)
        )



        top=self.cur.execute("""
        SELECT
        creator,
        reputation_score,
        category
        FROM creator_memory
        ORDER BY reputation_score DESC
        LIMIT 10
        """).fetchall()


        print("\nTOP MEMORY")


        for i,row in enumerate(top,1):

            print()
            print("#",i)
            print("Creator :",row[0])
            print("Score   :",row[1])
            print("Type    :",row[2])




if __name__=="__main__":

    engine=CreatorMemoryV25()

    engine.run()