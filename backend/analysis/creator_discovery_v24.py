import sqlite3
from collections import defaultdict


DB = "backend/database/tokens.db"


class CreatorDiscoveryV24:

    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.cur = self.conn.cursor()


    def load_creators(self):

        rows = self.cur.execute("""
            SELECT
                creator,
                name,
                symbol,
                market_cap_sol
            FROM tokens
            WHERE creator IS NOT NULL
        """).fetchall()

        creators = defaultdict(list)

        for r in rows:
            creators[r[0]].append({
                "name": r[1],
                "symbol": r[2],
                "mc": r[3] or 0
            })

        return creators


    def analyze_creator(self, creator, tokens):

        total = len(tokens)

        highest_mc = max(
            t["mc"] for t in tokens
        )

        avg_mc = sum(
            t["mc"] for t in tokens
        ) / total


        # MARKET STRENGTH
        market_strength = min(
            100,
            int(highest_mc / 50)
        )


        # BREAKOUT SIGNAL
        breakout = highest_mc >= 500


        # SURVIVOR
        survivor = highest_mc >= 100


        # PATTERN
        pattern = 100

        if total > 20:
            pattern -= 40

        if total > 50:
            pattern -= 20


        # DUPLICATE CHECK
        names = [
            t["name"]
            for t in tokens
            if t["name"]
        ]

        symbols = [
            t["symbol"]
            for t in tokens
            if t["symbol"]
        ]


        duplicate_penalty = 0


        if len(names) != len(set(names)):
            duplicate_penalty += 20


        if len(symbols) != len(set(symbols)):
            duplicate_penalty += 20


        pattern -= duplicate_penalty
        pattern = max(0, pattern)



        # RAW SCORE

        raw_score = (
            market_strength * 0.45
            +
            pattern * 0.35
            +
            (20 if breakout else 0)
        )


        raw_score = int(
            min(100, raw_score)
        )


        # HISTORY CONFIDENCE

        if total <= 2:
            history_weight = 0.35
            confidence = "LOW"

        elif total <=10:
            history_weight = 0.6
            confidence = "MEDIUM"

        else:
            history_weight = 1
            confidence = "HIGH"



        final_score = int(
            raw_score * history_weight
            +
            (100 * (1-history_weight))
            if total <=2
            else raw_score
        )


        # EARLY BOOST

        signals=[]

        if breakout:
            signals.append(
                "Breakout token detected"
            )

        if pattern >=80:
            signals.append(
                "Clean creator pattern"
            )

        if total <=2:
            signals.append(
                "Early creator"
            )


        if final_score >=85:
            decision="ALPHA CANDIDATE"

        elif final_score >=65:
            decision="WATCH LIST"

        else:
            decision="DANGER"



        return {
            "creator":creator,
            "score":final_score,
            "decision":decision,
            "confidence":confidence,
            "tokens":total,
            "highest":round(highest_mc,2),
            "average":round(avg_mc,2),
            "market_strength":market_strength,
            "pattern":pattern,
            "signals":signals
        }



    def run(self):

        creators=self.load_creators()

        results=[]

        for creator,tokens in creators.items():

            results.append(
                self.analyze_creator(
                    creator,
                    tokens
                )
            )


        results.sort(
            key=lambda x:x["score"],
            reverse=True
        )


        print("\n==============================")
        print(" CREATOR DISCOVERY V24 ")
        print("==============================")

        print(
            "Total Creator :",
            len(results)
        )


        print("\n==============================")
        print(" TOP ALPHA ")
        print("==============================")


        for i,r in enumerate(results[:10],1):

            print(
                f"""
#{i}
Creator      : {r['creator']}
Score        : {r['score']}
Decision     : {r['decision']}
Confidence   : {r['confidence']}
Tokens       : {r['tokens']}
Highest MC   : {r['highest']}
Average MC   : {r['average']}
Market       : {r['market_strength']}
Pattern      : {r['pattern']}
Signals      : {r['signals']}
"""
            )



if __name__=="__main__":

    engine=CreatorDiscoveryV24()

    engine.run()