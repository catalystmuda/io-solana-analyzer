import sqlite3


DB = "backend/database/tokens.db"


def main():

    print("==============================")
    print(" SMART WALLET RANKER V2 ")
    print("==============================")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
    SELECT
        creator,
        COUNT(*) as total_tokens,
        AVG(sol_amount) as avg_buy,
        MAX(market_cap_sol) as peak_mc
    FROM tokens
    GROUP BY creator
    HAVING total_tokens >= 3
    ORDER BY peak_mc DESC
    LIMIT 30
    """)


    rows = cur.fetchall()


    print("SMART WALLET SIGNAL")
    print("------------------------------")


    for i,row in enumerate(rows,1):

        creator,total,avg_buy,peak = row


        score = 0


        # creator aktif
        if total >= 5:
            score += 2


        # pernah membuat token besar
        if peak >= 100:
            score += 3


        # modal awal bagus
        if avg_buy >= 2:
            score += 2


        print("------------------------------")
        print("#",i)
        print("Creator :", creator)
        print("Launch  :", total)
        print("Avg Buy :", round(avg_buy,3))
        print("Peak MC :", round(peak,2))
        print("Score   :", score)


        if score >= 6:
            print("Signal  : 🔥 REAL SMART WALLET")


    conn.close()



if __name__ == "__main__":
    main()