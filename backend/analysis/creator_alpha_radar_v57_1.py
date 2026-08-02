import sqlite3


DB = "backend/database/tokens.db"


print("==============================")
print(" CREATOR ALPHA RADAR V57.1 ")
print(" DATABASE CONNECTED ENGINE ")
print("==============================")
print()



def load_creators():

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()


    cursor.execute("""
        SELECT
            creator,
            total_tokens,
            highest_mc,
            breakout_count,
            survivor_count,
            reputation_score,
            risk_score,
            category,
            signals
        FROM creator_memory
        ORDER BY highest_mc DESC
    """)


    rows = cursor.fetchall()


    conn.close()


    return rows





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







def calculate_alpha(row):


    (
        creator,
        tokens,
        mc,
        breakout,
        survivor,
        reputation,
        risk,
        category,
        signals
    ) = row



    score = 0

    found = []
    missing = []



    # survivor

    if survivor > 0:
        score += 30
        found.append("SURVIVOR")

    else:
        missing.append("NO SURVIVOR")



    # breakout

    if breakout > 0:
        score += 30
        found.append("BREAKOUT")

    else:
        missing.append("NO BREAKOUT")



    # market cap

    if mc >= 1000:

        score += 25
        found.append("ELITE MC")


    elif mc >=300:

        score +=15
        found.append("MC 300+")


    elif mc >=100:

        score +=10
        found.append("EARLY MC")


    else:

        missing.append("LOW MC")




    # reputation


    if reputation >=80:

        score +=15
        found.append("REPUTATION")


    elif reputation >=50:

        score +=8
        found.append("CREATOR HISTORY")




    # risk


    if risk >=50:

        score -=30
        missing.append("HIGH RISK")



    if tokens >20:

        score -=30
        missing.append("MANY TOKENS")



    if score <0:
        score=0



    return {

        "creator":creator,

        "score":score,

        "probability":min(score,100),

        "tokens":tokens,

        "market":mc_stage(mc),

        "mc":mc,

        "category":category,

        "signals":found,

        "missing":missing

    }







def main():


    data = load_creators()


    print("TOTAL :",len(data))

    print()



    results=[]


    for row in data:

        results.append(
            calculate_alpha(row)
        )



    results.sort(
        key=lambda x:x["score"],
        reverse=True
    )



    for i,r in enumerate(results[:50],1):

        print("#",i)

        print(
            "Creator :",
            r["creator"]
        )

        print(
            "Hunter Score :",
            r["score"]
        )

        print(
            "Alpha Probability :",
            r["probability"],
            "%"
        )

        print(
            "Market :",
            r["market"]
        )

        print(
            "Highest MC :",
            r["mc"]
        )

        print(
            "Category :",
            r["category"]
        )

        print(
            "Signals :",
            r["signals"]
        )

        print(
            "Missing :",
            r["missing"]
        )

        print("-"*30)





if __name__ == "__main__":

    main()