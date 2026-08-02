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



def confidence(sample, alpha):

    if alpha >= 80:
        return "VERY HIGH"

    elif alpha >= 50:
        return "HIGH"

    elif alpha >= 30:
        return "MEDIUM"

    return "LOW"



def creator_quality(tokens, survivor, breakout, reputation):

    score = 0


    if breakout:
        score += 30

    if survivor:
        score += 25


    if tokens <= 3:
        score += 20

    elif tokens <= 10:
        score += 10


    if reputation >= 80:
        score += 25

    elif reputation >= 50:
        score += 15


    return min(score,100)



def dna(mc, tokens, survivor, breakout):

    if breakout and survivor and tokens <= 3:
        return "ALPHA CREATOR"


    if survivor and tokens <= 5:
        return "SURVIVOR CREATOR"


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


    if breakout:
        score += 35
        signals.append("BREAKOUT")

    else:
        weakness.append("NO BREAKOUT")



    if survivor:
        score += 30
        signals.append("SURVIVOR")

    else:
        weakness.append("NO SURVIVOR")



    if mc >= 1000:
        score += 20
        signals.append("ELITE MC")

    elif mc >= 100:
        score += 10
        signals.append("GROWING MC")

    else:
        weakness.append("LOW MC")



    if tokens <= 3:
        score += 15
        signals.append("EARLY CREATOR")



    if reputation >= 80:
        score += 10
        signals.append("REPUTATION")



    return min(score,100), signals, weakness



def grade(score):

    if score >= 80:
        return "ELITE"

    elif score >= 50:
        return "WATCH"

    elif score >= 30:
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
    print(" CREATOR ALPHA RADAR V45 ")
    print("==============================")
    print()


    print("TOTAL :",len(rows))
    print()


    rank = 1


    results = []


    for r in rows:

        raw, signals, weakness = calculate(r)


        quality = creator_quality(
            r[2],
            r[6],
            r[5],
            r[7]
        )


        alpha = int(
            (raw * 0.7) +
            (quality * 0.3)
        )


        alpha = min(alpha,100)


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
        reverse=True,
        key=lambda x:x[0]
    )



    for item in results:


        alpha,r,raw,quality,signals,weakness=item


        print("#",rank)

        print("Creator :",r[1])

        print("Raw Score :",raw)

        print("Creator Quality :",quality)

        print("Alpha Score :",alpha)

        print("Alpha Probability :",alpha,"%")

        print("Grade :",grade(alpha))

        print("Confidence :",confidence(r[2],alpha))

        print("Tokens :",r[2])

        print("Market :",market_stage(r[3]))

        print("Highest MC :",r[3])

        print("DNA :",dna(
            r[3],
            r[2],
            r[6],
            r[5]
        ))

        print("Category :",r[9])

        print("Signals :",signals)

        print("Weakness :",weakness)

        print("------------------------------")


        rank += 1



    conn.close()



if __name__ == "__main__":

    main()