import sqlite3
import json


DB = "backend/database/tokens.db"


class CreatorMemoryV281:


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


        creators={}


        for creator,mc,name,symbol in rows:

            if creator not in creators:
                creators[creator]=[]


            creators[creator].append(
                {
                    "mc":mc or 0,
                    "name":name,
                    "symbol":symbol
                }
            )


        return creators




    def analyze(self,creator,tokens):


        total=len(tokens)


        mcs=[
            x["mc"]
            for x in tokens
        ]


        highest=max(mcs)

        average=sum(mcs)/total



        breakout=sum(
            1 for x in mcs
            if x>=500
        )


        survivor=sum(
            1 for x in mcs
            if x>=100
        )



        success=int(
            breakout/total*100
        )



        reputation=0
        risk=0

        signals=[]



        # breakout

        if breakout:

            reputation +=40

            signals.append(
                "Breakout history"
            )


        else:

            signals.append(
                "No breakout yet"
            )



        # history


        if total>=10:

            reputation +=20


            if success==0:

                risk+=50

                signals.append(
                    "Failed launch history"
                )

        else:

            reputation +=20

            signals.append(
                "Early creator"
            )



        # market


        if highest>=1000:

            reputation+=25

            signals.append(
                "Strong market history"
            )


        elif highest>=500:

            reputation+=15


        elif highest<50:

            risk+=10




        # survivor


        if survivor:

            reputation+=10



        # unknown adjustment


        if total==1 and breakout==0:

            reputation +=15

            risk -=10

            signals.append(
                "Unknown creator opportunity"
            )



        if risk<0:
            risk=0



        reputation=min(
            100,
            reputation
        )


        risk=min(
            100,
            risk
        )



        # category


        if breakout and total<=3:

            category="EARLY ALPHA"


        elif breakout and total>=10:

            category="SMART MONEY"


        elif total>=10 and success==0:

            category="DANGEROUS"


        elif total==1 and highest>=50:

            category="UNKNOWN PROMISING"


        elif total==1:

            category="UNKNOWN"



        elif reputation>=60:

            category="PROMISING"


        else:

            category="WATCH"




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
            "category":category,
            "grade":grade,
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


        for creator,tokens in creators.items():

            data=self.analyze(
                creator,
                tokens
            )

            self.save(data)

            results.append(data)



        self.conn.commit()



        results.sort(
            key=lambda x:x["reputation"],
            reverse=True
        )



        print("==============================")
        print(" CREATOR MEMORY V28.1 ")
        print("==============================")

        print(
            "Creators Updated:",
            len(results)
        )


        print("\nTOP MEMORY")


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

    CreatorMemoryV281().run()