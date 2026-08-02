import sqlite3


DB = "backend/database/tokens.db"



def market_stage(mc):

    if mc >= 1000:
        return "BREAKOUT"

    elif mc >= 200:
        return "GROWING"

    elif mc >= 50:
        return "EARLY"

    else:
        return "DEAD"



def confidence(alpha_score, tokens):

    if alpha_score >= 80 and tokens <= 3:
        return "VERY HIGH"

    elif alpha_score >= 60:
        return "HIGH"

    elif alpha_score >= 40:
        return "MEDIUM"

    elif alpha_score >= 20:
        return "LOW"

    return "VERY LOW"



def creator_quality(tokens, survivor, breakout, reputation):

    score = 0


    # creator history
    if tokens >= 50:
        score += 40

    elif tokens >= 20:
        score += 30

    elif tokens >= 10:
        score += 20

    else:
        score += 10



    # survival proof
    if survivor:
        score += 20



    # breakout proof
    if breakout:
        score += 20



    # reputation
    if reputation >= 80:
        score += 20


    return min(score,100)



def dna_creator(mc, tokens, survivor, breakout):


    if breakout and survivor and tokens <= 3:

        return "ALPHA CREATOR"



    if survivor and tokens <= 5:

        return "SURVIVOR"



    if tokens >= 20 and mc < 50:

        return "FAILED BUILDER"



    if mc < 50:

        return "FAILED"



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



    # breakout

    if breakout:

        score += 30

        signals.append("BREAKOUT")

    else:

        weakness.append("NO BREAKOUT")



    # survivor

    if survivor:

        score += 25

        signals.append("SURVIVOR")

    else:

        weakness.append("NO SURVIVOR")



    # market cap

    if mc >= 1000:

        score += 25

        signals.append("ELITE MC")


    elif mc >= 100:

        score += 15

        signals.append("GROWING MC")


    else:

        weakness.append("LOW MC")



    # early creator

    if tokens <= 3:

        score += 15

        signals.append("EARLY CREATOR")



    # reputation

    if reputation >= 80:

        score += 10

        signals.append("REPUTATION")



    return min(score,100), signals, weakness





def grade(score):


    if score >= 80:

        return "ELITE"


    elif score >= 50:

        return "WATCH"


    elif score >= 20:

        return "RISK"


    return "AVOID"





def main():


    conn = sqlite3.connect(DB)

    cur = conn.cursor()



    cur.execute("""
    SELECT *
    FROM creator_memory
    ORDER BY highest_mc DESC
    LIMIT 50
    """)



    rows = cur.fetchall()



    print("==============================")

    print(" CREATOR ALPHA RADAR V44 ")

    print("==============================")

    print()



    print("TOTAL :",len(rows))

    print()



    rank = 1



    for r in rows:


        raw, signals, weakness = calculate(r)



        quality = creator_quality(

            r[2],

            r[6],

            r[5],

            r[7]

        )



        alpha_score = int(

            (raw * 0.7) +

            (quality * 0.3)

        )



        alpha_score = min(alpha_score,100)



        probability = alpha_score



        dna = dna_creator(

            r[3],

            r[2],

            r[6],

            r[5]

        )



        print("#",rank)

        print("Creator :",r[1])

        print("Raw Score :",raw)

        print("Creator Quality :",quality)

        print("Alpha Score :",alpha_score)

        print("Alpha Probability :",probability,"%")

        print("Grade :",grade(alpha_score))

        print("Confidence :",confidence(alpha_score,r[2]))

        print("Tokens :",r[2])

        print("Market :",market_stage(r[3]))

        print("Highest MC :",r[3])

        print("DNA :",dna)

        print("Category :",r[9])

        print("Signals :",signals)

        print("Weakness :",weakness)

        print("------------------------------")



        rank += 1



    conn.close()





if __name__ == "__main__":

    main()