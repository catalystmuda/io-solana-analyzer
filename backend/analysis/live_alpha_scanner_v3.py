import sqlite3
from collections import defaultdict


DB="backend/database/tokens.db"


def main():

    print("==============================")
    print(" LIVE ALPHA SCANNER V3 ")
    print("==============================")


    conn=sqlite3.connect(DB)
    cur=conn.cursor()


    cur.execute("""
    SELECT
    creator,
    symbol,
    name,
    market_cap_sol,
    sol_amount,
    created_at
    FROM tokens
    """)


    rows=cur.fetchall()


    creators=defaultdict(list)


    for r in rows:
        creators[r[0]].append(r)


    results=[]


    for creator,tokens in creators.items():


        launches=len(tokens)

        peak_mc=max(
            x[3] for x in tokens
        )


        # cari token terbaru creator
        latest=sorted(
            tokens,
            key=lambda x:x[5],
            reverse=True
        )[0]


        symbol=latest[1]
        name=latest[2]
        mc=latest[3]
        sol=latest[4]
        time=latest[5]


        score=0


        # creator history
        if launches>=50:
            score+=4

        elif launches>=20:
            score+=3

        elif launches>=10:
            score+=2



        # previous success
        if peak_mc>=100:
            score+=3

        elif peak_mc>=50:
            score+=2



        # current token strength
        if sol>=5:
            score+=3

        elif sol>=2:
            score+=2



        results.append(
            (
            score,
            creator,
            launches,
            symbol,
            name,
            mc,
            sol,
            time,
            peak_mc
            )
        )


    results.sort(
        reverse=True
    )


    print("TOP CREATOR + TOKEN")
    print("------------------------------")


    for i,r in enumerate(results[:20],1):

        print(f"""
#{i}
Creator : {r[1]}
Launches: {r[2]}
TOKEN   : {r[3]}
NAME    : {r[4]}
MC SOL  : {round(r[5],2)}
BUY SOL : {round(r[6],3)}
Peak MC : {round(r[8],2)}
Score   : {r[0]}
------------------------------""")


if __name__=="__main__":
    main()