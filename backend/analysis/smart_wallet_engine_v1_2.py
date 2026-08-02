import sqlite3


DB = "backend/database/tokens.db"


print("==============================")
print(" SMART WALLET ENGINE V1.2 ")
print(" ALPHA CREATOR MEMORY MODE ")
print("==============================")


def connect():
    return sqlite3.connect(DB)



def classify(highest_mc, total, alpha):

    if highest_mc >= 1000:
        return "ELITE SMART CREATOR"

    elif highest_mc >= 300:
        return "ALPHA CREATOR"

    elif highest_mc >= 100:
        return "PROMISING WALLET"

    elif total >= 3:
        return "ACTIVE WALLET"

    return "NEW WALLET"



def run():

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    SELECT
        wallet,
        COUNT(*),
        SUM(
            CASE
            WHEN entry_mc >=100
            THEN 1
            ELSE 0
            END
        ),
        MAX(entry_mc)

    FROM wallet_activity

    GROUP BY wallet

    ORDER BY MAX(entry_mc) DESC

    LIMIT 50
    """)


    rows = cur.fetchall()


    print()
    print("TOTAL WALLETS :",len(rows))
    print()


    rank=1


    for r in rows:

        wallet=r[0]
        total=r[1]
        alpha=r[2] or 0
        highest=r[3] or 0


        win=round(
            (alpha/total)*100,
            2
        )


        print("#",rank)
        print("Wallet :",wallet)
        print("Trades :",total)
        print("Alpha Hits :",alpha)
        print("Win Rate :",win,"%")
        print("Highest MC :",highest)
        print("Reputation :",classify(highest,total,alpha))
        print("------------------------------")

        rank+=1


    conn.close()



if __name__=="__main__":
    run()