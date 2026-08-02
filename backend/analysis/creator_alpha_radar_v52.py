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

    if alpha >= 85:
        return "VERY HIGH"

    elif alpha >= 65:
        return "HIGH"

    elif alpha >= 45:
        return "MEDIUM"

    return "LOW"



def creator_quality(tokens, survivor, breakout, reputation):

    score = 0


    if breakout:
        score += 40


    if survivor:
        score += 30


    if tokens <= 3:
        score += 20


    if reputation >= 80:
        score += 10


    return min(score,100)



def history_power(tokens, mc):

    bonus = 0


    if tokens <=3:
        bonus +=10


    if mc >=1000:
        bonus +=20

    elif mc >=500:
        bonus +=15

    elif mc >=100:
        bonus +=10


    return bonus



def risk_penalty(
        breakout,
        survivor,
        reputation,
        mc):


    penalty = 0


    if not breakout:
        penalty +=15


    if not survivor:
        penalty +=20


    if reputation <80:
        penalty +=5


    if mc <100:
        penalty +=10


    return penalty



def creator_dna(
        mc,
        tokens,
        survivor,
        breakout):


    if breakout and survivor and tokens <=3:
        return "ALPHA CREATOR"


    if survivor and tokens <=3 and mc >=100:
        return "EARLY GEM"


    if survivor and mc >=100:
        return "PROMISING CREATOR"


    if mc <50:
        return "FAILED"


    return "UNKNOWN"



def category(dna):

    if dna=="ALPHA CREATOR":
        return "ELITE ALPHA"


    if dna=="EARLY GEM":
        return "EARLY WATCH"


    if dna=="PROMISING CREATOR":
        return "WATCHLIST"


    if dna=="FAILED":
        return "DEAD"


    return "UNKNOWN"



def grade(score):

    if score>=85:
        return "ELITE"

    elif score>=60:
        return "WATCH"

    elif score>=40:
        return "RISK"

    return "AVOID"



def calculate(row):


    tokens=row[2]
    mc=row[3]
    breakout=row[5]
    survivor=row[6]
    reputation=row[7]


    score=0
    signals=[]
    weakness=[]


    if breakout:
        score+=40
        signals.append("BREAKOUT")

    else:
        weakness.append("NO BREAKOUT")



    if survivor:
        score+=30
        signals.append("SURVIVOR")

    else:
        weakness.append("NO SURVIVOR")



    if mc>=1000:
        score+=20
        signals.append("ELITE MC")


    elif mc>=100:
        score+=10
        signals.append("GROWING MC")


    else:
        weakness.append("LOW MC")



    if tokens<=3:
        score+=10
        signals.append("EARLY CREATOR")



    if reputation>=80:
        signals.append("REPUTATION")



    quality=creator_quality(
        tokens,
        survivor,
        breakout,
        reputation
    )


    history=history_power(
        tokens,
        mc
    )


    penalty=risk_penalty(
        breakout,
        survivor,
        reputation,
        mc
    )


    alpha=(
        score
        +
        int(quality*0.10)
        +
        history
        -
        penalty
    )


    alpha=max(0,min(alpha,100))


    return (
        alpha,
        score,
        quality,
        history,
        penalty,
        signals,
        weakness
    )



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
    print(" CREATOR ALPHA RADAR V52 ")
    print("==============================")
    print()

    print("TOTAL :",len(rows))
    print()



    results=[]


    for r in rows:


        data=calculate(r)


        dna=creator_dna(
            r[3],
            r[2],
            r[6],
            r[5]
        )


        results.append(
            (
                data[0],
                r,
                data,
                dna
            )
        )



    results.sort(
        reverse=True,
        key=lambda x:x[0]
    )



    rank=1


    for item in results:


        alpha,r,data,dna=item


        print("#",rank)

        print("Creator :",r[1])

        print("Raw Score :",data[1])

        print("Creator Quality :",data[2])

        print("History Bonus :",data[3])

        print("Risk Penalty :",data[4])

        print("Alpha Score :",alpha)

        print("Alpha Probability :",alpha,"%")

        print("Grade :",grade(alpha))

        print("Confidence :",confidence(alpha))

        print("Tokens :",r[2])

        print("Market :",market_stage(r[3]))

        print("Highest MC :",r[3])

        print("DNA :",dna)

        print("Category :",category(dna))

        print("Signals :",data[5])

        print("Weakness :",data[6])

        print("------------------------------")


        rank+=1



    conn.close()



if __name__=="__main__":
    main()