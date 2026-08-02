import sqlite3
from collections import defaultdict

DB = "backend/database/tokens.db"


def main():

    print("==============================")
    print(" FINAL ALPHA HUNTER V2 ")
    print("==============================")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
    SELECT
        creator,
        symbol,
        name,
        market_cap_sol,
        sol_amount
    FROM tokens
    """)

    rows = cur.fetchall()


    creators = defaultdict(list)


    for r in rows:
        creators[r[0]].append({
            "symbol": r[1],
            "name": r[2],
            "mc": r[3] or 0,
            "sol": r[4] or 0
        })


    results=[]


    for creator,tokens in creators.items():

        launches=len(tokens)

        peak_mc=max(
            x["mc"] for x in tokens
        )

        avg_sol=sum(
            x["sol"] for x in tokens
        )/launches


        score=0


        # creator repeat
        if launches >=10:
            score+=2

        if launches >=30:
            score+=2


        # market performance
        if peak_mc >=40:
            score+=2

        if peak_mc >=70:
            score+=2


        # early buy quality
        if avg_sol >=3:
            score+=2


        if score>=6:
            signal="🔥 ALPHA HUNTER"
        else:
            signal=""


        results.append(
            (
            creator,
            launches,
            peak_mc,
            avg_sol,
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


    no=1

    for r in results[:20]:

        print(f"""
#{no}
Creator : {r[0]}
Launches: {r[1]}
Peak MC  : {round(r[2],2)}
Avg SOL  : {round(r[3],3)}
Score    : {r[4]}
Signal   : {r[5]}
------------------------------""")

        no+=1



if __name__=="__main__":
    main()