import sqlite3


DB = "backend/database/tokens.db"


print("==============================")
print(" SMART WALLET ENGINE V1.3 ")
print(" REPUTATION FILTER ENGINE ")
print("==============================")
print()


def reputation(trades, alpha_hits, highest_mc):

    if highest_mc >= 1000 and alpha_hits >= 1:
        return "ELITE SMART CREATOR"

    if highest_mc >= 300 and alpha_hits >= 1:
        return "ALPHA CREATOR"

    if highest_mc >= 100 and alpha_hits >= 1:
        return "PROMISING WALLET"

    if trades >= 20 and alpha_hits == 0:
        return "FACTORY CREATOR"

    if trades >= 5 and alpha_hits == 0:
        return "ACTIVE WALLET"

    return "NEW WALLET"



def run():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
    SELECT
        wallet,
        COUNT(*),
        SUM(
            CASE 
            WHEN exit_mc >= 100 THEN 1
            ELSE 0
            END
        ),
        MAX(exit_mc)
    FROM wallet_activity
    GROUP BY wallet
    ORDER BY MAX(exit_mc) DESC
    """)


    rows = cur.fetchall()


    print("TOTAL WALLETS :", len(rows))
    print()


    rank = 1


    for row in rows[:50]:

        wallet = row[0]
        trades = row[1]
        alpha_hits = row[2] or 0
        highest_mc = row[3] or 0


        rep = reputation(
            trades,
            alpha_hits,
            highest_mc
        )


        print("#",rank)
        print("Wallet :",wallet)
        print("Trades :",trades)
        print("Alpha Hits :",alpha_hits)
        print("Highest MC :",highest_mc)
        print("Reputation :",rep)
        print("------------------------------")

        rank += 1



if __name__ == "__main__":
    run()