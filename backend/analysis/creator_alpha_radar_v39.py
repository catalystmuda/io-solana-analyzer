import sqlite3


DB="backend/database/tokens.db"



# ==========================
# MARKET CLASSIFICATION
# ==========================

def market_stage(mc):

    if mc >= 1000:
        return "BREAKOUT"

    elif mc >= 200:
        return "GROWING"

    elif mc >=50:
        return "EARLY"

    else:
        return "DEAD"



# ==========================
# CONFIDENCE ENGINE
# ==========================

def confidence(sample):

    if sample>=20:
        return "HIGH"

    elif sample>=10:
        return "MEDIUM"

    elif sample>=5:
        return "LOW-MEDIUM"

    elif sample>=2:
        return "LOW"

    return "VERY LOW"



# ==========================
# CQI
# ==========================

def calculate_cqi(row):

    tokens=row[2]
    mc=row[3]


    if tokens<=0:
        return 0


    return round(
        mc/tokens,
        2
    )



# ==========================
# HIT RATE
# ==========================

def hit_rate(row):

    mc=row[3]


    if mc>=100:
        return 100

    return 0



# ==========================
# SURVIVOR SCORE
# ==========================

def survivor_score(row):

    survivor=row[6]


    if survivor:
        return 100

    return 0



# ==========================
# CREATOR TIER
# ==========================

def creator_tier(
        samples,
        cqi,
        score
):


    if (
        samples>=10
        and
        cqi>=500
        and
        score>=80
    ):
        return "S-TIER"



    if (
        samples>=5
        and
        cqi>=100
    ):
        return "A-TIER"



    if (
        samples<5
        and
        cqi>=100
    ):
        return "EARLY TALENT"



    return "UNKNOWN"



# ==========================
# CREATOR CLASS
# ==========================

def creator_class(
        tier,
        score
):

    if tier=="S-TIER":
        return "SMART MONEY"


    elif tier=="A-TIER":
        return "PROVEN CREATOR"


    elif tier=="EARLY TALENT":
        return "EARLY ALPHA"


    elif score>=40:
        return "WATCH"


    return "DANGEROUS"



# ==========================
# DECISION ENGINE
# ==========================

def decision(tier,score):


    if tier=="S-TIER":
        return "ENTRY WATCH"


    elif tier=="A-TIER":
        return "RESEARCH"


    elif tier=="EARLY TALENT":
        return "MONITOR HARD"


    elif score>=40:
        return "MONITOR"


    return "AVOID"



# ==========================
# SCORING
# ==========================

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
        signals.append(
            "Breakout history"
        )



    if survivor:

        score+=20
        signals.append(
            "Survivor history"
        )



    if mc>=500:

        score+=20

        signals.append(
            "Strong market history"
        )


    elif mc>=100:

        score+=10

        signals.append(
            "Growing market"
        )



    if tokens<=3:

        score+=15

        signals.append(
            "Early creator"
        )



    if reputation>=80:

        score+=10

        signals.append(
            "High reputation"
        )



    return min(score,100),signals



# ==========================
# CREATOR DNA
# ==========================

def creator_dna(row):

    mc=row[3]


    if mc>=1000:
        return "BREAKOUT CREATOR"


    elif mc>=200:
        return "GROWING CREATOR"


    elif mc>=50:
        return "EARLY CREATOR"


    return "FAILED PATTERN"




# ==========================
# MAIN
# ==========================

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
    print(" CREATOR ALPHA RADAR V39 ")
    print("==============================")
    print()



    print("TOTAL :",len(rows))
    print()



    rank=1



    for r in rows:


        score,signals=calculate(r)


        cqi=calculate_cqi(r)


        tier=creator_tier(
            r[2],
            cqi,
            score
        )


        print("#",rank)

        print("Creator :",r[1])

        print("Score :",score)

        print("Tier :",tier)

        print(
            "Class :",
            creator_class(
                tier,
                score
            )
        )


        print(
            "Decision :",
            decision(
                tier,
                score
            )
        )


        print(
            "Confidence :",
            confidence(r[2])
        )


        print(
            "CQI :",
            cqi
        )


        print(
            "Hit Rate :",
            hit_rate(r),
            "%"
        )


        print(
            "Survivor :",
            survivor_score(r),
            "%"
        )


        print(
            "Tokens :",
            r[2]
        )


        print(
            "Market :",
            market_stage(r[3])
        )


        print(
            "Highest MC :",
            r[3]
        )


        print(
            "DNA :",
            creator_dna(r)
        )


        print(
            "Category :",
            r[9]
        )


        print(
            "Signals :",
            signals
        )


        print("------------------------------")



        rank+=1



    conn.close()




if __name__=="__main__":
    main()