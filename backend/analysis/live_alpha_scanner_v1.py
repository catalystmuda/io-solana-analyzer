import sqlite3
from datetime import datetime


DB="backend/database/tokens.db"


SMART_CREATORS = [
"bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa",
"dtrzJPj7yDdvm6eRqBAgxsK2sMJeD9HhBEBB3XMedXy",
"8ua4kyudhLrQDKcAgaPhcRa8GHw7G9YgjBrZ19eVn1Hy"
]


def main():

    print("==============================")
    print(" LIVE ALPHA SCANNER V1 ")
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
    LIMIT 100
    """)


    rows=cur.fetchall()


    print("CANDIDATE")
    print("------------------------------")


    for r in rows:

        name,symbol,creator,mc,sol,time=r


        score=0


        if creator in SMART_CREATORS:
            score+=5


        if mc and mc < 100:
            score+=2


        if sol and sol >=2:
            score+=2


        if score>=5:

            print(f"""
TOKEN : {symbol}
NAME  : {name}
CREATOR : {creator}
MC SOL : {round(mc,2)}
BUY SOL: {round(sol,3)}
TIME : {time}
SCORE : {score}
SIGNAL : 🔥 WATCH
------------------------------""")


if __name__=="__main__":
    main()