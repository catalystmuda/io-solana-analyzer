import sqlite3


DB = "backend/database/tokens.db"


def main():

    print("==============================")
    print(" TOKEN DATABASE CHECK ")
    print("==============================")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
    SELECT COUNT(*)
    FROM tokens
    """)

    total = cur.fetchone()[0]

    print()
    print("TOTAL TOKENS :", total)


    cur.execute("""
    SELECT 
    name,
    symbol,
    creator,
    market_cap_sol
    FROM tokens
    ORDER BY id DESC
    LIMIT 10
    """)


    rows = cur.fetchall()


    print()
    print("LATEST TOKENS")
    print("----------------")


    for r in rows:
        print(
            "Name :", r[0],
            "| Symbol :", r[1],
            "| Creator :", r[2][:8],
            "| MC :", r[3]
        )


    conn.close()



if __name__ == "__main__":
    main()