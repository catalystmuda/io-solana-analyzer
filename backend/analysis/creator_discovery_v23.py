import sqlite3
from collections import Counter


DB_PATH = "backend/database/tokens.db"


class CreatorDiscoveryV23:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()


    def get_creators(self):

        self.cur.execute("""
            SELECT DISTINCT creator
            FROM tokens
            WHERE creator IS NOT NULL
        """)

        return [
            x[0]
            for x in self.cur.fetchall()
        ]


    def analyze_creator(self, creator):

        self.cur.execute("""
            SELECT
                name,
                symbol,
                market_cap_sol
            FROM tokens
            WHERE creator = ?
        """, (creator,))


        rows = self.cur.fetchall()


        total = len(rows)


        if total == 0:
            return None


        names = [
            x[0]
            for x in rows
            if x[0]
        ]

        symbols = [
            x[1]
            for x in rows
            if x[1]
        ]


        markets = [
            x[2]
            for x in rows
            if x[2]
        ]


        highest = max(markets) if markets else 0

        average = (
            sum(markets) / len(markets)
            if markets
            else 0
        )


        duplicate_name = (
            sum(
                c-1
                for c in Counter(names).values()
                if c > 1
            )
        )


        duplicate_symbol = (
            sum(
                c-1
                for c in Counter(symbols).values()
                if c > 1
            )
        )


        score = 50


        signals = []


        # alpha history
        if highest >= 500:
            score += 25
            signals.append(
                "Strong marketcap history"
            )


        if highest >= 100:
            score += 15
            signals.append(
                "Breakout token detected"
            )


        # creator health

        if total == 1:
            score += 10
            signals.append(
                "Early creator"
            )


        if total > 30:
            score -= 30
            signals.append(
                "Mass launch detected"
            )


        if duplicate_name > 5:
            score -= 15
            signals.append(
                "Duplicate token names"
            )


        if duplicate_symbol > 5:
            score -= 15
            signals.append(
                "Duplicate token symbols"
            )


        score = max(
            0,
            min(
                100,
                score
            )
        )


        if score >= 80:
            tier = "ALPHA CANDIDATE"

        elif score >= 55:
            tier = "WATCH LIST"

        else:
            tier = "DANGER"


        return {
            "creator": creator,
            "score": score,
            "tier": tier,
            "tokens": total,
            "highest": round(highest,2),
            "average": round(average,2),
            "signals": signals
        }



    def scan(self):

        creators = self.get_creators()

        results=[]


        for creator in creators:

            data = self.analyze_creator(
                creator
            )

            if data:
                results.append(data)


        return sorted(
            results,
            key=lambda x:x["score"],
            reverse=True
        )



if __name__ == "__main__":

    engine = CreatorDiscoveryV23()

    results = engine.scan()


    print()
    print("==============================")
    print(" CREATOR DISCOVERY V23 ")
    print("==============================")

    print(
        "Total Creator :",
        len(results)
    )


    print()
    print("==============================")
    print(" TOP ALPHA CANDIDATE ")
    print("==============================")


    count=0


    for r in results:

        if r["tier"]=="ALPHA CANDIDATE":

            count+=1

            print()
            print("#",count)
            print("Creator :",r["creator"])
            print("Score   :",r["score"])
            print("Tokens  :",r["tokens"])
            print("Highest :",r["highest"])
            print("Average :",r["average"])
            print("Signals :",r["signals"])


            if count>=10:
                break


    print()
    print("==============================")
    print(" WATCH LIST ")
    print("==============================")


    count=0

    for r in results:

        if r["tier"]=="WATCH LIST":

            count+=1

            print()
            print("#",count)
            print("Creator :",r["creator"])
            print("Score   :",r["score"])

            if count>=10:
                break


    print()
    print("==============================")
    print(" DANGER ")
    print("==============================")


    count=0

    for r in results:

        if r["tier"]=="DANGER":

            count+=1

            print()
            print("#",count)
            print("Creator :",r["creator"])
            print("Score   :",r["score"])

            if count>=10:
                break