import sqlite3


DB="backend/database/tokens.db"


def classify(score):

    if score >=85:
        return "SMART MONEY"

    if score >=55:
        return "EARLY OPPORTUNITY"

    if score >=35:
        return "WATCH"

    return "DANGEROUS"



def confidence(tokens):

    if tokens >=10:
        return "HIGH"

    if tokens >=3:
        return "MEDIUM"

    return "LOW"



def analyze(data):

    (
        creator,
        total_tokens,
        highest_mc,
        breakout,
        survivor,
        category,
        reputation,
        risk
    )=data


    score=0
    signals=[]


    # breakout
    if breakout>0:
        score+=35
        signals.append("Breakout history")


    # survivor
    if survivor>0:
        score+=25
        signals.append("Survivor history")


    # early creator
    if total_tokens<=3:
        score+=15
        signals.append("Early creator")


    # market quality
    if highest_mc>=500:
        score+=20
        signals.append("Strong market history")

    elif highest_mc>=100:
        score+=10
        signals.append("Growing market")


    # penalty only real danger

    if total_tokens>3 and survivor==0 and breakout==0:
        score-=20
        signals.append("No success history")


    if score<0:
        score=0


    if score>=85:
        decision="ENTRY WATCH"

    elif score>=55:
        decision="MONITOR"

    elif score>=35:
        decision="ACCUMULATING DATA"

    else:
        decision="AVOID"


    return {
        "creator":creator,
        "score":score,
        "class":classify(score),
        "decision":decision,
        "confidence":confidence(total_tokens),
        "tokens":total_tokens,
        "mc":highest_mc,
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
    print(" CREATOR ALPHA RADAR V36 ")
    print("==============================")

    print()

    print("TOTAL :",len(rows))


    rank=1

    for row in rows:

        r=analyze(row)

        print()

        print("#",rank)

        print("Creator :",r["creator"])

        print("Score :",r["score"])

        print("Class :",r["class"])

        print("Decision :",r["decision"])

        print("Confidence :",r["confidence"])

        print("Tokens :",r["tokens"])

        print("Highest MC :",r["mc"])

        print("Category :",r["category"])

        print("Signals :",r["signals"])

        print("------------------------------")

        rank+=1



if __name__=="__main__":
    main()