import sqlite3


DB = "backend/database/tokens.db"


def main():

    print("==============================")
    print(" SMART WALLET RANKER V1 ")
    print("==============================")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    print("SMART WALLET SIGNAL")
    print("------------------------------")


    cur.execute("""
    SELECT
        t.creator,
        t.symbol,
        t.name,
        t.market_cap_sol,
        t.sol_amount,
        COUNT(*) as creator_tokens
    FROM tokens t
    GROUP BY t.creator
    ORDER BY creator_tokens DESC
    LIMIT 20
    """)


    rows = cur.fetchall()


    for i,row in enumerate(rows,1):

        creator,symbol,name,mc,sol,count=row


        score = 0


        # creator repeat
        if count >= 2:
            score += 3


        # early buy strength
        if sol >= 2:
            score += 2


        # low MC
        if mc <= 50:
            score += 2


        print("------------------------------")
        print("#",i)
        print("Creator :",creator)
        print("Token   :",symbol)
        print("Name    :",name)
        print("MC SOL  :",round(mc,2))
        print("SOL Buy :",sol)
        print("Creator Tokens :",count)
        print("Score :",score)


        if score >=6:
            print("Signal : 🔥 SMART WALLET")


    conn.close()



if __name__=="__main__":
    main()