import sqlite3


DB="backend/database/tokens.db"



def market_stage(mc):

    if mc >= 1000:
        return "BREAKOUT"

    elif mc >= 200:
        return "GROWING"

    elif mc >=50:
        return "EARLY"

    else:
        return "DEAD"



def confidence(sample):

    if sample>=10:
        return "HIGH"

    elif sample>=5:
        return "MEDIUM"

    elif sample>=2:
        return "LOW"

    return "VERY LOW"



def creator_class(score):

    if score>=80:
        return "SMART MONEY"

    elif score>=50:
        return "PROMISING"

    elif score>=30:
        return "WATCH"

    else:
        return "DANGEROUS"



def decision(score):

    if score>=80:
        return "ENTRY WATCH"

    elif score>=50:
        return "MONITOR"

    elif score>=30:
        return "RESEARCH"

    return "AVOID"



def calculate(row):

    score=0
    signals=[]


    mc=row[3]
    breakout=row[5]
    survivor=row[6]
    reputation=row[7]
    tokens=row[2]


    if breakout:
        score+=30
        signals.append("Breakout history")


    if survivor:
        score+=20
        signals.append("Survivor history")


    if mc>=500:
        score+=20
        signals.append("Strong market history")

    elif mc>=100:
        score+=10
        signals.append("Growing market")


    if tokens<=3:
        score+=15
        signals.append("Early creator")


    if reputation>=80:
        score+=10
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
    print(" CREATOR ALPHA RADAR V38 ")
    print("==============================")
    print()

    print("TOTAL :",len(rows))
    print()


    rank=1


    for r in rows:

        score,signals=calculate(r)

        print("#",rank)

        print("Creator :",r[1])

        print("Score :",score)

        print("Class :",creator_class(score))

        print("Decision :",decision(score))

        print("Confidence :",confidence(r[2]))

        print("Tokens :",r[2])

        print("Market :",market_stage(r[3]))

        print("Highest MC :",r[3])

        print("Category :",r[9])

        print("Signals :",signals)

        print("------------------------------")


        rank+=1


    conn.close()



if __name__=="__main__":
    main()