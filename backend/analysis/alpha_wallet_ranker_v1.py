import sqlite3

DB = "backend/database/tokens.db"


def main():

    print("==============================")
    print(" ALPHA WALLET RANKER V1 ")
    print("==============================")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT
        creator,
        COUNT(*) as tokens,
        MAX(market_cap_sol) as peak_mc
    FROM tokens
    GROUP BY creator
    ORDER BY peak_mc DESC
    LIMIT 50
    """)

    rows = cur.fetchall()

    print("TOP CREATOR HISTORY")
    print("------------------------------")

    for i,r in enumerate(rows,1):

        creator, total, peak = r

        if peak >= 500:
            score = "ELITE"
        elif peak >= 100:
            score = "ALPHA"
        else:
            score = "NORMAL"

        print("#",i)
        print("Creator :",creator)
        print("Tokens  :",total)
        print("Peak MC :",round(peak,2))
        print("Rank    :",score)
        print("------------------------------")

    conn.close()


if __name__ == "__main__":
    main()