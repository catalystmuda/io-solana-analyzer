import sqlite3


DB = "backend/database/tokens.db"


def main():

    print("==============================")
    print(" ALPHA FILTER ENGINE V4 ")
    print("==============================")


    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
    SELECT
        creator,
        name,
        symbol,
        initial_buy,
        sol_amount,
        market_cap_sol,
        created_at
    FROM tokens
    ORDER BY id DESC
    LIMIT 100
    """)


    rows = cur.fetchall()


    print("TOP EARLY ALPHA")
    print("------------------------------")


    rank = 1

    for row in rows:

        creator = row[0]
        name = row[1]
        symbol = row[2]
        buy = row[3]
        sol = row[4]
        mc = row[5]


        score = 0


        # creator deploy dengan modal besar
        if sol >= 2:
            score += 3

        elif sol >= 1:
            score += 2


        # market cap awal sehat
        if mc >= 30:
            score += 2


        # initial buy besar
        if buy >= 50000000:
            score += 3


        if score >= 6:
            signal = "🔥 ALPHA"
        elif score >=4:
            signal = "WATCH"
        else:
            continue


        print("------------------------------")
        print("#",rank)
        print("Creator :",creator)
        print("Token   :",symbol)
        print("Name    :",name)
        print("MC SOL  :",round(mc,2))
        print("SOL Buy :",sol)
        print("Score   :",score)
        print("Signal  :",signal)


        rank += 1


        if rank > 20:
            break


    conn.close()


if __name__=="__main__":
    main()