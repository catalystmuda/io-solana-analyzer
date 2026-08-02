import sqlite3


DB="backend/database/tokens.db"


SMART_CREATORS=[
"bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa",
"dtrzJPj7yDdvm6eRqBAgxsK2sMJeD9HhBEBB3XMedXy",
"8ua4kyudhLrQDKcAgaPhcRa8GHw7G9YgjBrZ19eVn1Hy"
]


def main():

    print("==============================")
    print(" LIVE ALPHA SCANNER V2 ")
    print("==============================")


    conn=sqlite3.connect(DB)
    cur=conn.cursor()


    cur.execute("""
    SELECT
    name,
    symbol,
    creator,
    market_cap_sol,
    sol_amount,
    created_at
    FROM tokens
    ORDER BY id DESC
    LIMIT 200
    """)


    rows=cur.fetchall()


    result=[]


    for r in rows:

        name,symbol,creator,mc,sol,time=r


        if creator not in SMART_CREATORS:
            continue


        score=0


        # creator quality
        score+=5


        # early market cap
        if mc < 35:
            score+=3


        elif mc < 50:
            score+=2


        # buy strength
        if sol>=3:
            score+=3

        elif sol>=1:
            score+=2


        result.append(
            (
            score,
            symbol,
            name,
            creator,
            mc,
            sol,
            time
            )
        )


    result.sort(reverse=True)


    print("TOP ENTRY")
    print("------------------------------")


    for i,r in enumerate(result[:10],1):

        print(f"""
#{i}
TOKEN : {r[1]}
NAME  : {r[2]}
CREATOR : {r[3]}
MC SOL : {round(r[4],2)}
BUY SOL: {round(r[5],3)}
TIME : {r[6]}
SCORE : {r[0]}
SIGNAL : 🔥 ALPHA ENTRY
------------------------------""")


if __name__=="__main__":
    main()