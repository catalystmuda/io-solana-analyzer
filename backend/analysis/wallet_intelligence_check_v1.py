import sqlite3


DB = "backend/database/tokens.db"


def main():

    print("==============================")
    print(" WALLET INTELLIGENCE CHECK V1 ")
    print("==============================")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    print("\nTOTAL WALLET ACTIVITY")

    cur.execute("""
    SELECT COUNT(*)
    FROM wallet_activity
    """)

    total = cur.fetchone()[0]

    print(total)


    print("\nUNIQUE WALLETS")

    cur.execute("""
    SELECT COUNT(DISTINCT wallet)
    FROM wallet_activity
    """)

    wallets = cur.fetchone()[0]

    print(wallets)


    print("\nTOP ACTIVE WALLET")


    cur.execute("""
    SELECT wallet,
           COUNT(*) as trades
    FROM wallet_activity
    GROUP BY wallet
    ORDER BY trades DESC
    LIMIT 10
    """)


    for row in cur.fetchall():

        print(
            "Wallet:",
            row[0],
            "| Trades:",
            row[1]
        )


    print("\nENTRY MC SAMPLE")


    cur.execute("""
    SELECT wallet,
           token_symbol,
           entry_mc,
           roi,
           result
    FROM wallet_activity
    LIMIT 10
    """)


    for row in cur.fetchall():

        print(row)


    conn.close()



if __name__ == "__main__":
    main()