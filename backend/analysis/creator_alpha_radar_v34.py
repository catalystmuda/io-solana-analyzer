import sqlite3
import json
import sys


DB = "backend/database/tokens.db"


def confidence_level(total_tokens, breakout, survival):

    if total_tokens >= 5 and breakout >= 2 and survival >= 2:
        return "HIGH"

    if total_tokens >= 3 and breakout >= 1:
        return "MEDIUM"

    return "LOW"


def classify(score):

    if score >= 85:
        return "SMART MONEY"

    if score >= 60:
        return "WATCH"

    return "DANGEROUS"



def analyze():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
    SELECT
        creator,
        total_tokens,
        highest_mc,
        breakout_count,
        survivor_count,
        reputation_score,
        category
    FROM creator_memory
    ORDER BY reputation_score DESC
    """)


    rows = cur.fetchall()

    print("==============================")
    print(" CREATOR ALPHA RADAR V34 ")
    print("==============================")

    print()
    print("TOTAL CREATOR :", len(rows))
    print()


    rank = 1


    for r in rows[:20]:

        creator = r[0]
        total = r[1]
        highest = r[2]
        breakout = r[3]
        survivor = r[4]
        rep = r[5]
        category = r[6]


        score = rep


        confidence = confidence_level(
            total,
            breakout,
            survivor
        )


        signals=[]


        if breakout > 0:
            signals.append("Breakout history")

        if survivor > 0:
            signals.append("Survivor history")

        if total <= 2:
            signals.append("Early creator")


        if total >=3:
            signals.append("Creator consistency")


        print("#",rank)

        print("Creator :",creator)

        print("Score :",score)

        print(
            "Class :",
            classify(score)
        )

        print(
            "Confidence :",
            confidence
        )

        print(
            "Tokens :",
            total
        )

        print(
            "Highest MC :",
            highest
        )

        print(
            "Category :",
            category
        )

        print(
            "Signals :",
            signals
        )

        print("------------------------------")

        rank+=1


    conn.close()



if __name__=="__main__":

    analyze()