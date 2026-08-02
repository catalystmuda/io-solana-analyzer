import sqlite3
import os


DB_PATH = os.path.join(
    "backend",
    "database",
    "tokens.db"
)


BLACKLIST = [
    "WSOL",
    "SOL",
    "USDC",
    "USDT"
]


def load_tokens():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tokens
        ORDER BY rowid DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows



def safe(value):

    if value is None:
        return ""

    return str(value)



def score_token(row):

    score = 0


    # berdasarkan struktur database
    try:

        name = safe(row[3])
        symbol = safe(row[4])
        creator = safe(row[5])
        mc = float(row[9])
        buy = float(row[8])


    except Exception:

        return 0



    # market cap awal
    if mc >= 20:
        score += 2

    if mc >= 50:
        score += 1


    # early buyer
    if buy >= 1:
        score += 2

    if buy >= 5:
        score += 1


    # nama token ada
    if name:
        score += 1


    # creator ada
    if creator:
        score += 1


    return min(score,10)



def main():

    print("==============================")
    print(" LIVE ALPHA SCANNER V5 ")
    print("==============================")
    print("TOP ENTRY")
    print("------------------------------")


    tokens = load_tokens()


    results=[]


    for row in tokens:


        symbol = safe(row[4]).upper()


        if symbol in BLACKLIST:
            continue



        score = score_token(row)


        if score >=5:

            results.append(
                (
                    score,
                    row
                )
            )



    results.sort(
        key=lambda x:x[0],
        reverse=True
    )



    for rank,(score,row) in enumerate(results[:20],1):


        print()

        print(f"#{rank}")

        print("------------------------------")


        print(
            "TOKEN :",
            safe(row[3])
        )


        print(
            "SYMBOL:",
            safe(row[4])
        )


        print(
            "MINT  :",
            safe(row[1])
        )


        print(
            "CREATOR:",
            safe(row[5])
        )


        print(
            "MC SOL:",
            safe(row[9])
        )


        print(
            "BUY SOL:",
            safe(row[8])
        )


        print(
            "TIME:",
            safe(row[13])
        )


        print(
            "SCORE:",
            score
        )


        if score >=8:

            print(
                "SIGNAL : 🔥 ALPHA ENTRY"
            )

        else:

            print(
                "SIGNAL : 👀 WATCH"
            )


        print("------------------------------")




if __name__=="__main__":
    main()