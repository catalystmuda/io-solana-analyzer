import sqlite3


DB = "backend/database/tokens.db"



def market_stage(mc):

    if mc >= 1000:
        return "BREAKOUT"

    elif mc >= 300:
        return "MOMENTUM"

    elif mc >= 100:
        return "EARLY"

    elif mc >= 50:
        return "GENESIS"

    return "DEAD"





def confidence(score):

    if score >=85:
        return "VERY HIGH"

    elif score >=65:
        return "HIGH"

    elif score >=40:
        return "MEDIUM"

    return "LOW"





def lifecycle(mc,tokens,survivor,breakout):


    if breakout and survivor and mc>=1000:
        return "ALPHA CREATOR"



    if survivor and mc>=300:
        return "MOMENTUM GEM"



    if survivor and tokens<=3:
        return "EARLY GEM"



    if tokens<=3 and mc>=50:
        return "GENESIS"



    return "UNKNOWN"







def creator_quality(tokens,survivor,breakout,mc,reputation):


    score=0


    if survivor:
        score+=35


    if breakout:
        score+=30



    if tokens<=3:
        score+=20


    elif tokens<=10:
        score+=10


    else:
        score-=20



    if mc>=300:
        score+=10



    if reputation>=80:
        score+=5



    return max(0,min(score,100))







def track_record(mc,tokens,survivor,breakout):


    score=0



    if mc>=1000:
        score+=40

    elif mc>=500:
        score+=30

    elif mc>=300:
        score+=20

    elif mc>=100:
        score+=10



    if survivor:
        score+=25



    if tokens<=3:
        score+=15

    else:
        score-=10



    if breakout:
        score+=20



    return max(0,min(score,100))







def analyze(row):


    signals=[]
    weakness=[]

    score=0


    tokens=row[2]
    mc=row[3]
    breakout=row[5]
    survivor=row[6]
    reputation=row[7]



    if survivor:

        score+=35
        signals.append("SURVIVOR")

    else:

        weakness.append("NO SURVIVOR")



    if breakout:

        score+=30
        signals.append("BREAKOUT")

    else:

        weakness.append("NO BREAKOUT")





    if mc>=1000:

        score+=20
        signals.append("ELITE MC")


    elif mc>=300:

        score+=15
        signals.append("MOMENTUM MC")


    elif mc>=100:

        score+=10
        signals.append("EARLY MC")


    else:

        weakness.append("LOW MC")





    if tokens<=3:

        score+=10
        signals.append("LOW SUPPLY CREATOR")



    if reputation>=80:

        score+=5
        signals.append("REPUTATION")



    return score,signals,weakness







def grade(score):


    if score>=85:
        return "ELITE"

    elif score>=65:
        return "WATCH"

    elif score>=40:
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

    print(" CREATOR ALPHA RADAR V55 ")

    print("==============================")

    print()


    print("TOTAL :",len(rows))

    print()



    results=[]



    for row in rows:


        raw,signals,weakness=analyze(row)



        quality=creator_quality(
            row[2],
            row[6],
            row[5],
            row[3],
            row[7]
        )


        history=track_record(
            row[3],
            row[2],
            row[6],
            row[5]
        )



        alpha=int(
            raw*0.45
            +
            quality*0.30
            +
            history*0.25
        )



        results.append(
            (
                alpha,
                row,
                raw,
                quality,
                history,
                signals,
                weakness
            )
        )





    results.sort(
        key=lambda x:x[0],
        reverse=True
    )



    rank=1



    for item in results:


        alpha,row,raw,quality,history,signals,weakness=item


        print("#",rank)

        print("Creator :",row[1])

        print("Raw Score :",raw)

        print("Creator Quality :",quality)

        print("Track Record :",history)

        print("Alpha Score :",alpha)

        print("Alpha Probability :",alpha,"%")

        print("Grade :",grade(alpha))

        print("Confidence :",confidence(alpha))

        print("Tokens :",row[2])

        print("Market :",market_stage(row[3]))

        print("Highest MC :",row[3])

        print("DNA :",lifecycle(
            row[3],
            row[2],
            row[6],
            row[5]
        ))

        print("Category :",row[9])

        print("Signals :",signals)

        print("Weakness :",weakness)

        print("------------------------------")


        rank+=1




    conn.close()





if __name__=="__main__":

    main()