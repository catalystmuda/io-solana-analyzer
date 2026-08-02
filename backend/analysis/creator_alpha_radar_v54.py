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

    elif alpha >= 60:
        return "HIGH"

    elif alpha >= 40:
        return "MEDIUM"

    return "LOW"



def creator_track_record(mc,tokens,survivor,breakout):

    score = 0


    # historical achievement

    if mc >= 1000:
        score += 40

    elif mc >= 500:
        score +=25

    elif mc >=200:
        score +=15



    # survival proof

    if survivor:
        score +=20



    # breakout proof

    if breakout:
        score +=20



    # creator discipline

    if tokens <=3:
        score +=20

    elif tokens <=10:
        score +=10

    else:
        score -=20



    return max(0,min(score,100))





def creator_quality(tokens,survivor,breakout,reputation):

    score=0


    if breakout:
        score+=35


    if survivor:
        score+=30



    if tokens <=3:
        score+=20

    elif tokens <=10:
        score+=10

    else:
        score-=20



    if reputation>=80:
        score+=15


    return max(0,min(score,100))





def creator_dna(mc,tokens,survivor,breakout):


    if breakout and survivor and tokens<=3:
        return "ALPHA CREATOR"



    if survivor and mc>=200:
        return "EARLY GEM"



    if survivor:
        return "SURVIVOR"



    if mc<50:
        return "FAILED"



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

        score+=25
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

        score+=5
        signals.append("REPUTATION")



    return score,signals,weakness






def grade(score):

    if score>=85:
        return "ELITE"

    elif score>=60:
        return "WATCH"

    elif score>=30:
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
    print(" CREATOR ALPHA RADAR V54 ")
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



        track=creator_track_record(
            r[3],
            r[2],
            r[6],
            r[5]
        )



        alpha=int(
            (raw*0.50)
            +
            (quality*0.25)
            +
            (track*0.25)
        )



        alpha=min(alpha,100)



        results.append(
            (
                alpha,
                r,
                raw,
                quality,
                track,
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


        alpha,r,raw,quality,track,signals,weakness=x



        print("#",rank)

        print("Creator :",r[1])

        print("Raw Score :",raw)

        print("Creator Quality :",quality)

        print("Track Record Score :",track)

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