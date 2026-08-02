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



def confidence(sample):

    if sample >= 20:
        return "VERY HIGH"

    elif sample >= 10:
        return "HIGH"

    elif sample >= 5:
        return "MEDIUM"

    elif sample >= 2:
        return "LOW"

    return "VERY LOW"



def reliability(tokens):

    if tokens >= 20:
        return 100

    elif tokens >= 10:
        return 80

    elif tokens >= 5:
        return 60

    elif tokens >= 3:
        return 40

    else:
        return 20



def risk_level(tokens, mc):

    if tokens >= 20 and mc >= 500:
        return "LOW"

    elif tokens >= 5:
        return "MEDIUM"

    elif tokens <= 2:
        return "HIGH"

    return "UNKNOWN"



def creator_class(score):

    if score >= 80:
        return "SMART MONEY"

    elif score >= 50:
        return "PROMISING"

    elif score >= 30:
        return "WATCH"

    else:
        return "DANGEROUS"



def decision(score):

    if score >= 80:
        return "ELITE WATCH"

    elif score >= 60:
        return "EARLY HUNTER"

    elif score >= 40:
        return "RESEARCH"

    elif score >= 20:
        return "RISK"

    return "AVOID"



def creator_dna(mc, tokens, survivor, breakout):

    if breakout and mc >= 1000 and tokens <= 3:
        return "ONE HIT WONDER"

    if breakout and survivor:
        return "BREAKOUT CREATOR"

    if survivor and tokens >= 5:
        return "CONSISTENT BUILDER"

    if mc < 50:
        return "FAILED PATTERN"

    return "UNKNOWN"



def calculate(row):

    score = 0
    signals = []

    mc = row[3]
    breakout = row[5]
    survivor = row[6]
    reputation = row[7]
    tokens = row[2]


    if breakout:
        score += 30
        signals.append("Breakout history")


    if survivor:
        score += 20
        signals.append("Survivor history")


    if mc >= 500:
        score += 20
        signals.append("Strong market history")

    elif mc >= 100:
        score += 10
        signals.append("Growing market")


    if tokens <= 3:
        score += 15
        signals.append("Early creator")


    if reputation >= 80:
        score += 10
        signals.append("High reputation")


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
    print(" CREATOR ALPHA RADAR V40 ")
    print("==============================")
    print()

    print("TOTAL :", len(rows))
    print()


    rank = 1


    for r in rows:

        raw_score, signals = calculate(r)

        rel = reliability(r[2])

        alpha_score = int(raw_score * (rel / 100))

        risk = risk_level(r[2], r[3])

        dna = creator_dna(
            r[3],
            r[2],
            r[6],
            r[5]
        )


        print("#", rank)

        print("Creator :", r[1])

        print("Raw Score :", raw_score)

        print("Reliability :", rel,"%")

        print("Alpha Score :", alpha_score)

        print("Tier :", decision(alpha_score))

        print("Class :", creator_class(alpha_score))

        print("Confidence :", confidence(r[2]))

        print("Risk :", risk)

        print("Tokens :", r[2])

        print("Market :", market_stage(r[3]))

        print("Highest MC :", r[3])

        print("DNA :", dna)

        print("Category :", r[9])

        print("Signals :", signals)

        print("------------------------------")


        rank += 1


    conn.close()



if __name__ == "__main__":
    main()