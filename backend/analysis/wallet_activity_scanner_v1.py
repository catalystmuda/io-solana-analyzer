import sqlite3
from datetime import datetime


DB = "backend/database/tokens.db"


print("==============================")
print(" WALLET ACTIVITY SCANNER V1 ")
print("==============================")


def connect():

    return sqlite3.connect(DB)



def scan_wallet_activity():

    conn = connect()
    cur = conn.cursor()


    print("\nREAD TOKENS DATABASE")


    cur.execute("""
        SELECT
            creator,
            mint,
            symbol,
            name,
            market_cap_sol,
            signature
        FROM tokens
    """)


    rows = cur.fetchall()


    print("TOKENS FOUND :", len(rows))


    inserted = 0


    for row in rows:

        creator = row[0]
        mint = row[1]
        symbol = row[2]
        name = row[3]
        mc = row[4]
        signature = row[5]


        if creator is None:
            continue


        try:

            cur.execute("""
                INSERT INTO wallet_activity
                (
                    wallet,
                    token_mint,
                    token_symbol,
                    token_name,
                    creator,
                    signature,
                    entry_mc,
                    exit_mc,
                    roi,
                    result,
                    buy_time
                )

                VALUES
                (?,?,?,?,?,?,?,?,?,?,?)
            """,

            (
                creator,
                mint,
                symbol,
                name,
                creator,
                signature,
                mc,
                mc,
                0,
                "UNKNOWN",
                datetime.utcnow()
            ))


            inserted += 1


        except Exception as e:

            pass



    conn.commit()


    print()
    print("==============================")
    print(" WALLET ACTIVITY COMPLETE ")
    print("==============================")

    print("INSERTED :", inserted)


    conn.close()



if __name__ == "__main__":

    scan_wallet_activity()