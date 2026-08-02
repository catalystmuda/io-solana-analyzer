import sqlite3
from collections import defaultdict


DB="backend/database/tokens.db"


def main():

    print("==============================")
    print(" FINAL ALPHA HUNTER V3 ")
    print("==============================")


    conn=sqlite3.connect(DB)
    cur=conn.cursor()


    cur.execute("""
    SELECT
        creator,
        symbol,
        name,
        market_cap_sol,
        sol_amount
    FROM tokens
    """)


    rows=cur.fetchall()


    creators=defaultdict(list)


    for r in rows:

        creators[r[0]].append({
            "symbol":r[1],
            "name":r[2],
            "mc":r[3] or 0,
            "sol":r[4] or 0
        })



    results=[]


    for creator,tokens in creators.items():

        launches=len(tokens)

        peak=max(
            x["mc"] for x in tokens
        )

        avg=sum(
            x["sol"] for x in tokens
        )/launches



        score=0


        # creator reputation
        if launches >= 10:
            score+=3

        if launches >=30:
            score+=2


        # performance
        if peak>=50:
            score+=2

        if peak>=100:
            score+=3


        # capital quality
        if avg>=5:
            score+=2


        # classify

        if launches>=10 and score>=7:
            signal="🔥 SMART CREATOR"

        elif launches<10 and peak>=100:
            signal="⚡ FRESH ALPHA"

        else:
            signal=""



        results.append(
            (
            creator,
            launches,
            peak,
            avg,
            score,
            signal
            )
        )



    results.sort(
        key=lambda x:x[4],
        reverse=True
    )



    print("RESULT")
    print("------------------------------")


    i=1

    for r in results[:30]:

        if r[5]:

            print(f"""
#{i}
Creator : {r[0]}
Launches: {r[1]}
Peak MC  : {round(r[2],2)}
Avg SOL  : {round(r[3],3)}
Score    : {r[4]}
Signal   : {r[5]}
------------------------------""")

            i+=1



if __name__=="__main__":
    main()