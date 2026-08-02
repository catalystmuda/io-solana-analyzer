import sqlite3

DB = "backend/database/tokens.db"


def main():

    print("==============================")
    print(" ALPHA SIGNAL ENGINE V1 ")
    print("==============================")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT
        creator,
        symbol,
        market_cap_sol
    FROM tokens
    ORDER BY market_cap_sol ASC
    LIMIT 100
    """)

    rows = cur.fetchall()

    print("EARLY ALPHA SCAN")
    print("------------------------------")

    for i, row in enumerate(rows,1):

        creator, symbol, mc = row

        if mc < 50:
            signal = "EARLY BUY WATCH"
        elif mc < 100:
            signal = "GROWTH WATCH"
        else:
            signal = "LATE"

        print("#",i)
        print("Creator :", creator)
        print("Token   :", symbol)
        print("MC      :", round(mc,2))
        print("Signal  :", signal)
        print("------------------------------")


    conn.close()


if __name__ == "__main__":
    main()