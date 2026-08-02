import sqlite3

DB = "backend/database/tokens.db"

def main():

    print("==============================")
    print(" SMART WALLET SIGNAL ENGINE V1 ")
    print("==============================")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT 
        creator,
        symbol,
        market_cap_sol
    FROM tokens
    ORDER BY market_cap_sol DESC
    LIMIT 50
    """)

    rows = cur.fetchall()

    print("TOP EARLY SIGNALS")
    print("------------------------------")

    for i,row in enumerate(rows,1):

        creator, symbol, mc = row

        if mc >= 100:
            signal = "ALPHA"
        elif mc >= 50:
            signal = "WATCH"
        else:
            signal = "NORMAL"

        print(f"#{i}")
        print("Creator :", creator)
        print("Token   :", symbol)
        print("MC      :", round(mc,2))
        print("Signal  :", signal)
        print("------------------------------")

    conn.close()


if __name__ == "__main__":
    main()