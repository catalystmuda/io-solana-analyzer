import sqlite3
import json


DB = "backend/database/tokens.db"


class CreatorMemoryV28:


    def __init__(self):

        self.conn = sqlite3.connect(DB)
        self.cur = self.conn.cursor()



    def load_creators(self):

        rows = self.cur.execute("""
            SELECT
                creator,
                market_cap_sol
            FROM tokens
            WHERE creator IS NOT NULL
        """).fetchall()


        creators={}


        for creator,mc in rows:

            if creator not in creators:
                creators[creator]=[]


            creators[creator].append(
                mc or 0
            )


        return creators




    def analyze(self,creator,values):


        total=len(values)


        highest=max(values)


        average=sum(values)/total


        breakout=sum(
            1 for x in values
            if x >=500
        )


        survivor=sum(
            1 for x in values
            if x >=100
        )



        success=int(
            breakout/total*100
        )



        reputation=0
        risk=0
        signals=[]



        # BREAKOUT VALUE

        if breakout:

            reputation +=40

            signals.append(
                "Breakout history"
            )


        else:

            risk +=20



        # HISTORY


        if total>=10:

            reputation +=20


            if success>=30:

                signals.append(
                    "Reliable creator"
                )

            else:

                risk +=40

                signals.append(
                    "Many failed launches"
                )



        else:

            reputation +=15

            signals.append(
                "Early creator"
            )



        # MARKET


        if highest>=1000:

            reputation +=25

            signals.append(
                "Strong market history"
            )


        elif highest>=500:

            reputation +=15



        else:

            risk +=10



        # SURVIVAL


        if survivor:

            reputation +=10


        else:

            risk +=10




        reputation=min(
            100,
            reputation
        )


        risk=min(
            100,
            risk
        )



        # CATEGORY


        if breakout and total<=3:

            category="EARLY ALPHA"


        elif breakout and total>=10:

            category="SMART MONEY"


        elif total>=20 and success==0:

            category="DANGEROUS"


        elif reputation>=60:

            category="PROMISING"


        elif total<=3:

            category="UNKNOWN"


        else:

            category="WATCH"



        # GRADE


        if reputation>=90:
            grade="A+"

        elif reputation>=75:
            grade="A"

        elif reputation>=60:
            grade="B"

        elif reputation>=40:
            grade="C"

        else:
            grade="D"



        return {

            "creator":creator,
            "total":total,
            "highest":highest,
            "average":average,
            "breakout":breakout,
            "survivor":survivor,
            "success":success,
            "reputation":reputation,
            "risk":risk,
            "grade":grade,
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
        data["category"],
        json.dumps(data["signals"])
        ))





    def run(self):


        creators=self.load_creators()

        results=[]


        for creator,values in creators.items():

            result=self.analyze(
                creator,
                values
            )

            self.save(result)

            results.append(result)



        self.conn.commit()



        results.sort(
            key=lambda x:x["reputation"],
            reverse=True
        )



        print("==============================")
        print(" CREATOR MEMORY V28 ")
        print("==============================")

        print(
            "Creators Updated:",
            len(results)
        )



        print("\nTOP SMART MEMORY")


        for i,r in enumerate(results[:10],1):

            print()

            print("#",i)

            print(
                "Creator:",
                r["creator"]
            )

            print(
                "Grade:",
                r["grade"]
            )

            print(
                "Class:",
                r["category"]
            )

            print(
                "Rep:",
                r["reputation"]
            )

            print(
                "Risk:",
                r["risk"]
            )

            print(
                "Success:",
                str(r["success"])+"%"
            )

            print(
                "Signals:",
                r["signals"]
            )



if __name__=="__main__":

    CreatorMemoryV28().run()