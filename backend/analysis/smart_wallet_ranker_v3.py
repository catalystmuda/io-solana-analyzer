import sqlite3


DB = "backend/database/tokens.db"


def main():

    print("==============================")
    print(" SMART WALLET RANKER V3 ")
    print("==============================")


    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
    SELECT
        creator,
        COUNT(*) as launches,
        MAX(market_cap_sol) as max_mc,
        AVG(sol_amount) as avg_sol
    FROM tokens
    GROUP BY creator
    ORDER BY launches DESC
    LIMIT 50
    """)


    rows = cur.fetchall()


    print("SMART WALLET ALPHA")
    print("------------------------------")


    results=[]


    for row in rows:

        creator, launches, max_mc, avg_sol = row


        score=0


        # creator repeat launcher
        if launches >= 10:
            score += 3
        elif launches >= 5:
            score += 2


        # pernah push MC tinggi
        if max_mc >= 100:
            score += 5
        elif max_mc >= 50:
            score += 3


        # modal entry
        if avg_sol >= 3:
            score += 2


        results.append(
            (
                score,
                creator,
                launches,
                max_mc,
                avg_sol
            )
        )


    results.sort(reverse=True)


    for i,item in enumerate(results[:20],1):

        score,creator,launches,max_mc,avg_sol=item


        print("------------------------------")
        print("#",i)
        print("Creator :",creator)
        print("Launches:",launches)
        print("Max MC  :",round(max_mc,2))
        print("Avg SOL :",round(avg_sol,3))
        print("Score   :",score)


        if score >=7:
            print("Signal  : 🔥 SMART WALLET ALPHA")


    conn.close()



if __name__=="__main__":
    main()