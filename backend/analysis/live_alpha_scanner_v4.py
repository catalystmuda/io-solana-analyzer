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



def score_token(row):

    score = 0


    # cari angka market cap dan buy dari data row
    numbers = []

    for x in row:

        try:
            numbers.append(float(x))
        except:
            pass


    if len(numbers) > 0:

        mc = max(numbers)

        if mc >= 20:
            score += 2

        if mc >= 50:
            score += 2



    for n in numbers:

        if n >= 1:
            score += 1

        if n >= 5:
            score += 2



    return min(score,10)




def main():

    print("==============================")
    print(" LIVE ALPHA SCANNER V4 ")
    print("==============================")
    print("TOP ENTRY")
    print("------------------------------")


    tokens = load_tokens()


    results=[]


    for row in tokens:


        text = " ".join(
            str(x)
            for x in row
            if x is not None
        )


        symbol = str(row[1]) if len(row)>1 else ""


        if symbol.upper() in BLACKLIST:
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



    for i,(score,row) in enumerate(results[:20],1):

        print()

        print(f"#{i}")

        print("------------------------------")

        for idx,value in enumerate(row):

            print(
                f"{idx}: {value}"
            )


        print("SCORE :",score)


        if score>=8:
            print("SIGNAL : 🔥 ALPHA ENTRY")

        else:
            print("SIGNAL : 👀 WATCH")

        print("------------------------------")



if __name__=="__main__":
    main()