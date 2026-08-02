import sqlite3


DB = "backend/database/tokens.db"



def market_stage(mc):

    if mc >= 1000:
        return "BREAKOUT"

    elif mc >= 200:
        return "GROWING"

    elif mc >= 50:
        return "EARLY"

    return "DEAD"



def confidence(alpha):

    if alpha >= 80:
        return "VERY HIGH"

    elif alpha >= 50:
        return "HIGH"

    elif alpha >= 30:
        return "MEDIUM"

    return "LOW"



def grade(score):

    if score >= 80:
        return "ELITE"

    elif score >= 50:
        return "WATCH"

    elif score >= 30:
        return "RISK"

    return "AVOID"



def creator_dna(mc,tokens,survivor,breakout):

    if breakout and survivor and tokens <=3:
        return "ALPHA CREATOR"

    if breakout:
        return "BREAKOUT CREATOR"

    if survivor and tokens <=3:
        return "EARLY GEM"

    if survivor:
        return "SURVIVOR"

    return "UNKNOWN"



def calculate(row):

    score = 0
    signals = []
    weakness = []


    tokens = row[2]
    mc = row[3]
    breakout = row[5]
    survivor = row[6]
    reputation = row[7]


    # BREAKOUT

    if breakout:
        score += 40
        signals.append("BREAKOUT")

    else:
        weakness.append("NO BREAKOUT")



    # SURVIVOR

    if survivor:
        score += 25
        signals.append("SURVIVOR")

    else:
        weakness.append("NO SURVIVOR")



    # MARKET CAP

    if mc >= 1000:

        score += 20
        signals.append("ELITE MC")

    elif mc >=100:

        score +=10
        signals.append("GROWING MC")

    else:

        weakness.append("LOW MC")



    # EARLY CREATOR

    if tokens <=3:

        score +=10
        signals.append("EARLY CREATOR")

    elif tokens >20:

        score -=10
        weakness.append("TOO MANY TOKENS")



    # REPUTATION

    if reputation >=80:

        score +=5
        signals.append("REPUTATION")



    return score,signals,weakness



def creator_quality(row):

    tokens=row[2]
    survivor=row[6]
    breakout=row[5]
    reputation=row[7]


    score=0


    if breakout:
        score+=40


    if survivor:
        score+=30


    if tokens<=3:
        score+=20


    if reputation>=80:
        score+=10


    return min(score,100)



def history_bonus(row):

    mc=row[3]
    tokens=row[2]


    bonus=0


    if mc>=1000:
        bonus+=30

    elif mc>=500:
        bonus+=25

    elif mc>=200:
        bonus+=20

    else:
        bonus+=10



    if tokens<=3:
        bonus+=10



    return min(bonus,40)



def risk_penalty(row):

    penalty=0

    tokens=row[2]
    mc=row[3]
    survivor=row[6]


    if tokens>20:
        penalty+=30


    if mc<50:
        penalty+=30


    if not survivor:
        penalty+=20


    return min(penalty,50)



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
    print(" CREATOR ALPHA RADAR V53 ")
    print("==============================")
    print()


    print("TOTAL :",len(rows))
    print()



    results=[]


    for r in rows:


        raw,signals,weakness=calculate(r)


        quality=creator_quality(r)


        history=history_bonus(r)


        penalty=risk_penalty(r)



        alpha = raw + history - penalty


        alpha=int(
            (alpha*0.65)+(quality*0.35)
        )


        alpha=max(0,min(alpha,100))



        results.append(
            (
                alpha,
                r,
                raw,
                quality,
                history,
                penalty,
                signals,
                weakness
            )
        )



    results.sort(
        reverse=True,
        key=lambda x:x[0]
    )



    rank=1


    for x in results:


        alpha,r,raw,quality,history,penalty,signals,weakness=x


        print("#",rank)

        print("Creator :",r[1])

        print("Raw Score :",raw)

        print("Creator Quality :",quality)

        print("History Bonus :",history)

        print("Risk Penalty :",penalty)

        print("Alpha Score :",alpha)

        print("Alpha Probability :",alpha,"%")

        print("Grade :",grade(alpha))

        print("Confidence :",confidence(alpha))

        print("Tokens :",r[2])

        print("Market :",market_stage(r[3]))

        print("Highest MC :",r[3])

        print("DNA :",creator_dna(
            r[3],
            r[2],
            r[6],
            r[5]
        ))

        print("Category :",r[9])

        print("Signals :",signals)

        print("Weakness :",weakness)

        print("------------------------------")


        rank+=1



    conn.close()



if __name__=="__main__":

    main()