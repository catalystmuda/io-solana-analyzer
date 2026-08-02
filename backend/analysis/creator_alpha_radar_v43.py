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



def confidence(tokens, survivor, breakout, mc):

    score = 0

    if survivor:
        score += 30

    if breakout:
        score += 30

    if mc >= 500:
        score += 25

    elif mc >= 100:
        score += 15


    if tokens >= 10:
        score += 15


    if score >= 80:
        return "VERY HIGH"

    elif score >= 60:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    return "LOW"



def creator_quality(tokens, survivor, breakout):

    score = 0


    if tokens >= 20:
        score += 40

    elif tokens >= 10:
        score += 30

    elif tokens >= 5:
        score += 20

    else:
        score += 10



    if survivor:
        score += 30


    if breakout:
        score += 30


    return min(score,100)



def grade(score):

    if score >= 85:
        return "ELITE"

    elif score >= 70:
        return "ALPHA"

    elif score >= 50:
        return "PROMISING"

    elif score >= 30:
        return "WATCH"

    elif score >= 15:
        return "RISK"

    return "AVOID"



def dna(mc,tokens,survivor,breakout):

    if breakout and survivor and tokens <=3:
        return "ALPHA CREATOR"

    if breakout and survivor:
        return "BREAKOUT BUILDER"

    if survivor:
        return "SURVIVOR"

    if mc < 50:
        return "FAILED"

    return "UNKNOWN"



def calculate(row):

    score = 0
    signals=[]
    weakness=[]


    tokens=row[2]
    mc=row[3]
    breakout=row[5]
    survivor=row[6]
    reputation=row[7]



    if breakout:
        score+=30
        signals.append("BREAKOUT")
    else:
        weakness.append("NO BREAKOUT")



    if survivor:
        score+=25
        signals.append("SURVIVOR")
    else:
        weakness.append("NO SURVIVOR")



    if mc>=1000:
        score+=25
        signals.append("ELITE MC")

    elif mc>=500:
        score+=20
        signals.append("HIGH MC")

    elif mc>=100:
        score+=10
        signals.append("GROWING MC")

    else:
        weakness.append("LOW MC")



    if tokens<=3:
        score+=15
        signals.append("EARLY CREATOR")


    elif tokens>=10:
        score+=10
        signals.append("EXPERIENCED")

    else:
        weakness.append("LIMITED HISTORY")



    if reputation>=80:
        score+=10
        signals.append("REPUTATION")



    return min(score,100),signals,weakness




def main():

    conn=sqlite3.connect(DB)

    cur=conn.cursor()


    cur.execute("""
    SELECT *
    FROM creator_memory
    """)


    rows=cur.fetchall()



    results=[]


    for r in rows:


        raw,signals,weakness=calculate(r)


        quality=creator_quality(
            r[2],
            r[6],
            r[5]
        )


        alpha=int(
            (raw*0.6)+(quality*0.4)
        )


        results.append(
            (
                alpha,
                r,
                raw,
                quality,
                signals,
                weakness
            )
        )



    results.sort(
        key=lambda x:x[0],
        reverse=True
    )



    print("==============================")
    print(" CREATOR ALPHA RADAR V43 ")
    print("==============================")
    print()


    print("TOTAL :",len(results[:50]))
    print()



    rank=1


    for item in results[:50]:

        alpha,r,raw,quality,signals,weakness=item


        print("#",rank)

        print("Creator :",r[1])

        print("Raw Score :",raw)

        print("Creator Quality :",quality)

        print("Alpha Score :",alpha)

        print("Alpha Probability :",str(alpha)+"%")

        print("Grade :",grade(alpha))

        print(
            "Confidence :",
            confidence(
                r[2],
                r[6],
                r[5],
                r[3]
            )
        )


        print("Tokens :",r[2])

        print("Market :",market_stage(r[3]))

        print("Highest MC :",r[3])

        print(
            "DNA :",
            dna(
                r[3],
                r[2],
                r[6],
                r[5]
            )
        )


        print("Category :",r[9])

        print("Signals :",signals)

        print("Weakness :",weakness)

        print("------------------------------")


        rank+=1



    conn.close()



if __name__=="__main__":

    main()