import sqlite3
import json


DB = "backend/database/tokens.db"


def grade(score):

    if score >= 85:
        return "SMART MONEY"

    if score >= 55:
        return "PROMISING"

    if score >= 35:
        return "UNKNOWN"

    return "DANGEROUS"



def confidence(sample):

    if sample >= 10:
        return "HIGH"

    if sample >= 5:
        return "MEDIUM"

    return "LOW"



def analyze(row):

    (
        creator,
        total_tokens,
        highest_mc,
        breakout,
        survivor,
        category,
        reputation,
        risk
    ) = row


    score = 0
    signals=[]


    # breakout history
    if breakout > 0:
        score += 35
        signals.append("Breakout history")


    # survival
    if survivor > 0:
        score += 20
        signals.append("Survivor history")


    # creator age
    if total_tokens <= 3:
        score += 15
        signals.append("Early creator")


    # market quality
    if highest_mc >= 500:
        score += 20
        signals.append("Strong market history")


    # multiple launch bonus
    if total_tokens >= 5:
        score += 10
        signals.append("Multiple token history")


    # risk reduction
    score -= risk


    if score < 0:
        score = 0


    # confidence adjustment
    conf = confidence(total_tokens)


    # category decision

    if score >= 85:
        decision="ENTRY WATCH"

    elif score >=55:
        decision="WATCH LIST"

    else:
        decision="AVOID"



    return {
        "creator":creator,
        "score":score,
        "class":grade(score),
        "decision":decision,
        "confidence":conf,
        "tokens":total_tokens,
        "highest_mc":highest_mc,
        "category":category,
        "signals":signals
    }




def main():

    conn=sqlite3.connect(DB)

    cur=conn.cursor()


    cur.execute("""
    SELECT
    creator,
    total_tokens,
    highest_mc,
    breakout_count,
    survivor_count,
    category,
    reputation_score,
    risk_score

    FROM creator_memory
    ORDER BY reputation_score DESC
    LIMIT 50
    """)


    rows=cur.fetchall()

    conn.close()


    print("==============================")
    print(" CREATOR ALPHA RADAR V35 ")
    print("==============================")

    print()

    print("TOTAL ANALYZED :",len(rows))


    rank=1


    for r in rows:

        data=analyze(r)

        print()

        print("#",rank)

        print("Creator :",data["creator"])

        print("Score :",data["score"])

        print("Class :",data["class"])

        print("Decision :",data["decision"])

        print("Confidence :",data["confidence"])

        print("Tokens :",data["tokens"])

        print("Highest MC :",data["highest_mc"])

        print("Category :",data["category"])

        print("Signals :",data["signals"])

        print("------------------------------")


        rank+=1



if __name__=="__main__":
    main()