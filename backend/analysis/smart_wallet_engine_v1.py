import sqlite3


DB = "backend/database/tokens.db"



def calculate_wallet_score(
        total_trades,
        alpha_hits,
        average_roi
):

    score = 0
    signals = []


    if total_trades >= 5:
        score += 20
        signals.append("EXPERIENCED WALLET")


    if alpha_hits >= 2:
        score += 40
        signals.append("ALPHA HISTORY")


    if average_roi >= 5:
        score += 30
        signals.append("HIGH ROI")


    if total_trades <= 1:
        score -= 10
        signals.append("NEW WALLET")


    if score < 0:
        score = 0


    return score, signals





def reputation(score):

    if score >=80:
        return "SMART MONEY"


    elif score >=50:
        return "PROMISING"


    elif score >=20:
        return "WATCH"


    return "UNKNOWN"







def analyze():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()


    cursor.execute("""
    SELECT
    wallet,
    total_trades,
    alpha_hits,
    average_roi,
    best_token,
    best_roi

    FROM smart_wallet_memory
    """)


    rows = cursor.fetchall()


    print("==============================")
    print(" SMART WALLET ENGINE V1 ")
    print("==============================")


    print()

    print("TOTAL WALLETS :", len(rows))

    print()


    rank = []


    for row in rows:


        wallet = row[0]
        trades = row[1]
        hits = row[2]
        roi = row[3]
        token = row[4]
        best_roi = row[5]


        score, signals = calculate_wallet_score(
            trades,
            hits,
            roi
        )


        rep = reputation(score)


        rank.append(
            (
                score,
                wallet,
                rep,
                signals,
                token,
                best_roi
            )
        )



    rank.sort(
        reverse=True,
        key=lambda x:x[0]
    )



    for i,item in enumerate(rank[:20],1):

        print("#",i)

        print("Wallet :",item[1])

        print("Smart Score :",item[0])

        print("Reputation :",item[2])

        print("Best Token :",item[4])

        print("Best ROI :",item[5])

        print("Signals :",item[3])

        print("------------------------------")



    conn.close()



if __name__ == "__main__":
    analyze()