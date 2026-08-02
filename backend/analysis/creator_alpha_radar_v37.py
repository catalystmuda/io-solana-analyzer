import sqlite3
import json


DB = "backend/database/tokens.db"


def confidence(sample):

    if sample >= 5:
        return "HIGH"

    elif sample >= 3:
        return "MEDIUM"

    elif sample >= 2:
        return "LOW-MEDIUM"

    else:
        return "VERY LOW"


def classify(score):

    if score >= 80:
        return "SMART MONEY"

    elif score >= 50:
        return "WATCH"

    else:
        return "DANGEROUS"



def calculate_score(row):

    score = 0
    signals=[]


    highest_mc=row[3]
    breakout=row[5]
    survivor=row[6]
    reputation=row[7]


    if breakout > 0:
        score +=30
        signals.append("Breakout history")


    if survivor > 0:
        score +=20
        signals.append("Survivor history")


    if highest_mc > 500:
        score +=20
        signals.append("Strong market history")


    elif highest_mc >100:
        score +=10
        signals.append("Growing market")


    if row[2] <=3:
        score +=15
        signals.append("Early creator")


    if reputation >=80:
        score +=10
        signals.append("High reputation")


    return min(score,100),signals



def main():

    conn=sqlite3.connect(DB)
    cur=conn.cursor()


    cur.execute("""
    SELECT *
    FROM creator_memory
    ORDER BY highest_mc DESC
    LIMIT 50
    """)


    rows=cur.fetchall()


    print("==============================")
    print(" CREATOR ALPHA RADAR V37 ")
    print("==============================")
    print()

    print("TOTAL :",len(rows))
    print()


    rank=1


    for row in rows:


        score,signals=calculate_score(row)


        sample=row[2]

        conf=confidence(sample)

        cls=classify(score)


        if score>=80:
            decision="ENTRY WATCH"

        elif score>=50:
            decision="ACCUMULATING DATA"

        else:
            decision="AVOID"



        print("#",rank)

        print("Creator :",row[1])

        print("Score :",score)

        print("Class :",cls)

        print("Decision :",decision)

        print("Confidence :",conf)

        print("Samples :",sample)

        print("Highest MC :",row[3])

        print("Category :",row[9])

        print("Signals :",signals)

        print("------------------------------")

        rank+=1



    conn.close()



if __name__=="__main__":
    main()