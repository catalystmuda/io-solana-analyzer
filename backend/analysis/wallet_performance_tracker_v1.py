import sqlite3


DB = "backend/database/tokens.db"


print("==============================")
print(" WALLET PERFORMANCE TRACKER V1 ")
print("==============================")


def main():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
    SELECT
        wallet,
        COUNT(*),
        MAX(entry_mc),
        MAX(exit_mc)
    FROM wallet_activity
    GROUP BY wallet
    ORDER BY MAX(exit_mc) DESC
    """)


    rows = cur.fetchall()


    print()
    print("TOTAL WALLETS :", len(rows))
    print()


    rank = 1


    for row in rows[:50]:

        wallet = row[0]
        trades = row[1]
        entry = row[2] or 0
        highest = row[3] or 0


        if entry > 0:
            roi = ((highest-entry)/entry)*100
        else:
            roi = 0


        if roi >= 500:
            category = "SMART MONEY"

        elif roi >= 100:
            category = "GOOD WALLET"

        elif roi > 0:
            category = "ACTIVE"

        else:
            category = "UNKNOWN"


        print("#", rank)
        print("Wallet :", wallet)
        print("Trades :", trades)
        print("Entry MC :", entry)
        print("Highest MC :", highest)
        print("ROI :", round(roi,2), "%")
        print("Category :", category)
        print("------------------------------")

        rank += 1


    conn.close()



if __name__ == "__main__":
    main()