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



def confidence(tokens):

    if tokens >= 50:
        return "VERY HIGH"
    elif tokens >= 20:
        return "HIGH"
    elif tokens >= 5:
        return "MEDIUM"
    elif tokens >= 2:
        return "LOW"

    return "VERY LOW"



def creator_quality(tokens, survivor, breakout, mc):

    score = 0


    # pengalaman creator
    if tokens >= 50:
        score += 30
    elif tokens >= 20:
        score += 25
    elif tokens >= 10:
        score += 20
    elif tokens >= 5:
        score += 10
    else:
        score += 5


    # creator pernah bertahan
    if survivor:
        score += 25


    # pernah breakout
    if breakout:
        score += 30


    # market proof
    if mc >= 1000:
        score += 15
    elif mc >= 500:
        score += 10


    return min(score,100)



def alpha_grade(score):

    if score >= 85:
        return "ELITE"

    elif score >= 70:
        return "STRONG"

    elif score >= 50:
        return "WATCH"

    elif score >= 30:
        return "RISK"

    return "AVOID"



def creator_dna(tokens, survivor, breakout, mc):

    if breakout and survivor and tokens <= 5:
        return "ALPHA CREATOR"

    if breakout and survivor:
        return "BREAKOUT CREATOR"

    if survivor and tokens >= 10:
        return "PRO BUILDER"

    if mc < 50:
        return "FAILED"

    return "UNKNOWN"



def calculate(row):

    tokens = row[2]
    mc = row[3]
    breakout = row[5]
    survivor = row[6]
    reputation = row[7]


    score = 0
    signals = []


    if breakout:
        score += 35
        signals.append("BREAKOUT")


    if survivor:
        score += 25
        signals.append("SURVIVOR")


    if tokens <= 5:
        score += 15
        signals.append("EARLY CREATOR")


    if mc >= 1000:
        score += 15
        signals.append("HIGH MC")


    elif mc >= 200:
        score += 10
        signals.append("GROWING MC")


    if reputation >= 80:
        score += 10
        signals.append("REPUTATION")


    return min(score,100), signals



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
    print(" CREATOR ALPHA RADAR V42 ")
    print("==============================")
    print()


    print("TOTAL :",len(rows))
    print()


    rank = 1


    for r in rows:


        raw, signals = calculate(r)


        quality = creator_quality(
            r[2],
            r[6],
            r[5],
            r[3]
        )


        final_score = int(
            (raw * 0.6) +
            (quality * 0.4)
        )


        dna = creator_dna(
            r[2],
            r[6],
            r[5],
            r[3]
        )


        print("#",rank)

        print("Creator :",r[1])

        print("Raw Score :",raw)

        print("Creator Quality :",quality)

        print("Alpha Score :",final_score)

        print("Grade :",alpha_grade(final_score))

        print("Confidence :",confidence(r[2]))

        print("Tokens :",r[2])

        print("Market :",market_stage(r[3]))

        print("Highest MC :",r[3])

        print("DNA :",dna)

        print("Category :",r[9])

        print("Signals :",signals)

        print("------------------------------")


        rank += 1


    conn.close()



if __name__ == "__main__":
    main()