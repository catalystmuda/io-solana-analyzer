import sqlite3


DB = "backend/database/tokens.db"


def main():

    print("==============================")
    print(" FINAL ALPHA HUNTER DEBUG V2 ")
    print("==============================")


    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
    SELECT
        t.name,
        t.symbol,
        t.creator,
        t.market_cap_sol,
        t.sol_amount,
        COUNT(t2.id),
        MAX(t2.market_cap_sol)

    FROM tokens t

    JOIN tokens t2
    ON t.creator = t2.creator

    GROUP BY t.id

    ORDER BY COUNT(t2.id) DESC

    LIMIT 20
    """)


    rows = cur.fetchall()


    print("RESULT")
    print("------------------------------")


    for i,r in enumerate(rows,1):

        name,symbol,creator,mc,sol,launches,peak = r


        score = 0


        if launches >= 10:
            score += 3

        if peak >= 50:
            score += 3

        if sol >= 3:
            score += 2


        print("------------------------------")
        print("#",i)
        print("Token :",symbol)
        print("Name :",name)
        print("Launch :",launches)
        print("Peak MC :",round(peak,2))
        print("Buy SOL :",round(sol,3))
        print("Score :",score)



    conn.close()



if __name__ == "__main__":
    main()