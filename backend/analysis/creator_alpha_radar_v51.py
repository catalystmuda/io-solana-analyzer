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

    elif alpha >= 60:
        return "HIGH"

    elif alpha >= 40:
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
        bonus += 10


    if mc >=1000:
        bonus +=10

    elif mc >=500:
        bonus +=8

    elif mc >=100:
        bonus +=5


    return bonus



def creator_dna(mc,tokens,survivor,breakout):

    if breakout and survivor and tokens <=3:
        return "ALPHA CREATOR"


    if survivor and tokens <=3 and mc >=100:
        return "EARLY GEM"


    if survivor and mc >=100:
        return "PROMISING CREATOR"


    if breakout:
        return "BREAKOUT CREATOR"


    if survivor:
        return "SURVIVOR"


    if mc <50:
        return "FAILED"


    return "UNKNOWN"



def category(dna):

    if dna=="ALPHA CREATOR":
        return "ELITE ALPHA"

    if dna=="EARLY GEM":
        return "EARLY ALPHA"

    if dna=="PROMISING CREATOR":
        return "WATCHLIST"

    if dna=="FAILED":
        return "DEAD"


    return "UNKNOWN"



def calculate(row):

    score=0
    signals=[]
    weakness=[]


    tokens=row[2]
    mc=row[3]
    breakout=row[5]
    survivor=row[6]
    reputation=row[7]


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


    return min(score,100),signals,weakness



def grade(alpha):

    if alpha>=80:
        return "ELITE"

    elif alpha>=60:
        return "WATCH"

    elif alpha>=40:
        return "RISK"

    return "AVOID"



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
    print(" CREATOR ALPHA RADAR V51 ")
    print("==============================")
    print()

    print("TOTAL :",len(rows))
    print()


    results=[]


    for r in rows:


        raw,signals,weakness=calculate(r)


        quality=creator_quality(
            r[2],
            r[6],
            r[5],
            r[7]
        )


        history=history_power(
            r[2],
            r[3]
        )


        alpha=min(
            raw + int(quality*0.10) + history,
            100
        )


        dna=creator_dna(
            r[3],
            r[2],
            r[6],
            r[5]
        )


        results.append(
            (
                alpha,
                r,
                raw,
                quality,
                history,
                dna,
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

        alpha,r,raw,quality,history,dna,signals,weakness=x


        print("#",rank)
        print("Creator :",r[1])
        print("Raw Score :",raw)
        print("Creator Quality :",quality)
        print("Creator History Bonus :",history)
        print("Alpha Score :",alpha)
        print("Alpha Probability :",alpha,"%")
        print("Grade :",grade(alpha))
        print("Confidence :",confidence(alpha))
        print("Tokens :",r[2])
        print("Market :",market_stage(r[3]))
        print("Highest MC :",r[3])
        print("DNA :",dna)
        print("Category :",category(dna))
        print("Signals :",signals)
        print("Weakness :",weakness)
        print("------------------------------")


        rank+=1



    conn.close()



if __name__=="__main__":
    main()