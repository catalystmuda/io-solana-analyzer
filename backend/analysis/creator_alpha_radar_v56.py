import sqlite3


DB = "backend/database/tokens.db"



def mc_stage(mc):

    if mc >= 1000:
        return "BREAKOUT"

    elif mc >= 300:
        return "MOMENTUM"

    elif mc >= 100:
        return "EARLY"

    elif mc >= 50:
        return "GENESIS"

    return "DEAD"




def risk_level(risk):

    if risk <=20:
        return "LOW"

    elif risk <=50:
        return "MEDIUM"

    return "HIGH"





def opportunity(alpha):

    if alpha >=90:
        return "ELITE ALPHA"

    elif alpha >=75:
        return "HIGH ALPHA"

    elif alpha >=60:
        return "PROMISING"

    elif alpha >=40:
        return "EARLY WATCH"

    return "UNKNOWN"






def dna(mc,survivor,breakout,tokens):


    if breakout and survivor and mc>=1000:
        return "ALPHA CREATOR"


    if survivor and mc>=300:
        return "MOMENTUM GEM"


    if survivor and tokens<=3:
        return "EARLY GEM"


    if tokens<=3:
        return "GENESIS"


    return "UNKNOWN"







def analyze(row):


    creator=row[1]
    tokens=row[2]
    mc=row[3]
    breakout=row[5]
    survivor=row[6]
    reputation=row[7]



    signals=[]
    missing=[]


    base=0



    # survival

    if survivor:

        base+=30
        signals.append("SURVIVOR")

    else:

        missing.append("NO SURVIVOR")




    # breakout

    if breakout:

        base+=25
        signals.append("BREAKOUT")

    else:

        missing.append("NO BREAKOUT")





    # MC quality

    if mc>=1000:

        base+=20
        signals.append("ELITE MC")


    elif mc>=300:

        base+=15
        signals.append("MC 300+")


    elif mc>=100:

        base+=10
        signals.append("EARLY MC")


    else:

        missing.append("LOW MC")





    # creator concentration

    if tokens==1:

        base+=15
        signals.append("SINGLE TOKEN")


    elif tokens<=3:

        base+=10
        signals.append("LOW TOKEN COUNT")


    else:

        missing.append("MANY TOKENS")





    if reputation>=80:

        base+=10
        signals.append("REPUTATION")





    # risk

    risk=0



    if not survivor:
        risk+=40


    if tokens>10:
        risk+=30


    if mc<100:
        risk+=20


    if not breakout:
        risk+=10





    # hunter adjustment

    hunter=int(
        base
        -
        (risk*0.25)
    )



    hunter=max(
        0,
        min(hunter,100)
    )



    return (
        hunter,
        risk,
        signals,
        missing
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

    print(" CREATOR ALPHA RADAR V56 ")

    print(" ALPHA HUNTER ENGINE ")

    print("==============================")

    print()


    print("TOTAL :",len(rows))

    print()



    results=[]



    for row in rows:


        hunter,risk,signals,missing=analyze(row)


        results.append(
            (
                hunter,
                row,
                risk,
                signals,
                missing
            )
        )



    results.sort(
        key=lambda x:x[0],
        reverse=True
    )



    rank=1



    for item in results:


        hunter,row,risk,signals,missing=item


        print("#",rank)

        print("Creator :",row[1])

        print("Hunter Score :",hunter)

        print("Alpha Probability :",hunter,"%")

        print("Opportunity :",opportunity(hunter))

        print("Risk Level :",risk_level(risk))

        print("Tokens :",row[2])

        print("Market :",mc_stage(row[3]))

        print("Highest MC :",row[3])

        print("DNA :",dna(
            row[3],
            row[6],
            row[5],
            row[2]
        ))

        print("Signals :",signals)

        print("Missing :",missing)

        print("------------------------------")


        rank+=1



    conn.close()






if __name__=="__main__":

    main()