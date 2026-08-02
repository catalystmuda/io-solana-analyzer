import sqlite3


DB = "backend/database/tokens.db"


print("==============================")
print(" SMART WALLET ENGINE V1.1 ")
print(" CREATOR PROXY MODE ")
print("==============================")


def connect():
    return sqlite3.connect(DB)



def classify_wallet(total, alpha, win_rate):

    if alpha >= 3 and win_rate >= 70:
        return "ELITE SMART MONEY"

    elif alpha >= 2:
        return "SMART WALLET"

    elif total >= 3:
        return "ACTIVE WALLET"

    return "NEW WALLET"



def run():

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    SELECT
        wallet,
        COUNT(*) as total,
        SUM(
            CASE
            WHEN entry_mc >= 100
            THEN 1
            ELSE 0
            END
        ) as alpha_hits,

        MAX(entry_mc)

    FROM wallet_activity

    GROUP BY wallet

    ORDER BY alpha_hits DESC

    LIMIT 50
    """)


    rows = cur.fetchall()


    print()
    print("TOTAL WALLETS :", len(rows))
    print()


    rank = 1


    for row in rows:

        wallet = row[0]
        total = row[1]
        alpha = row[2]
        highest = row[3]


        if alpha is None:
            alpha = 0


        win_rate = round(
            (alpha / total) * 100,
            2
        )


        reputation = classify_wallet(
            total,
            alpha,
            win_rate
        )


        print("#", rank)
        print("Wallet :", wallet)
        print("Trades :", total)
        print("Alpha Hits :", alpha)
        print("Win Rate :", win_rate,"%")
        print("Highest MC :", highest)
        print("Reputation :", reputation)
        print("------------------------------")


        rank += 1



    conn.close()



if __name__ == "__main__":
    run()