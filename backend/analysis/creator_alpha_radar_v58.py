import sqlite3


DB = "backend/database/tokens.db"



print("==============================")
print(" CREATOR ALPHA RADAR V58 ")
print(" EARLY SIGNAL DETECTOR ")
print("==============================\n")



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




def opportunity(score):

    if score >=80:
        return "ALPHA WATCH"

    elif score >=50:
        return "EARLY SIGNAL"

    elif score >=30:
        return "WATCH"

    return "IGNORE"




def calculate_alpha(
    highest_mc,
    survivor,
    breakout,
    reputation,
    tokens
):

    score = 0
    signals = []
    missing = []


    # survivor
    if survivor:
        score += 30
        signals.append("SURVIVOR")
    else:
        missing.append("NO SURVIVOR")



    # reputation creator
    if reputation >=70:
        score +=25
        signals.append("REPUTATION")

    elif reputation >=40:
        score +=10
        signals.append("KNOWN CREATOR")



    # early market advantage

    if highest_mc >=100 and highest_mc <500:

        score +=20
        signals.append("EARLY MC")



    elif highest_mc >=500:

        score -=10



    # breakout

    if breakout:

        score +=25
        signals.append("BREAKOUT")

    else:

        missing.append("NO BREAKOUT")



    # creator focus

    if tokens <=3:

        score +=10
        signals.append("LOW TOKEN CREATOR")

    else:

        score -=10



    if score <0:
        score=0


    return score,signals,missing




def category(score,mc):

    if score>=80:

        return "ALPHA BEFORE EXPLOSION"


    if score>=50:

        return "EARLY DISCOVERY"


    if mc<100:

        return "TOO EARLY"


    return "LOW QUALITY"





conn=sqlite3.connect(DB)

cur=conn.cursor()


query="""

SELECT
creator,
total_tokens,
highest_mc,
breakout_count,
survivor_count,
reputation_score

FROM creator_memory

"""


rows=cur.execute(query).fetchall()


results=[]



for r in rows:


    creator=r[0]
    tokens=r[1]
    mc=r[2]

    breakout = r[3] > 0

    survivor = r[4] > 0

    reputation = r[5]



    score,signals,missing = calculate_alpha(
        mc,
        survivor,
        breakout,
        reputation,
        tokens
    )


    results.append({

        "creator":creator,
        "score":score,
        "mc":mc,
        "tokens":tokens,
        "signals":signals,
        "missing":missing

    })




results.sort(
    key=lambda x:x["score"],
    reverse=True
)



print("TOTAL :",len(results))
print()



rank=1


for r in results[:50]:


    print("#",rank)

    print("Creator :",r["creator"])

    print("Hunter Score :",r["score"])

    print(
        "Opportunity :",
        opportunity(r["score"])
    )


    print(
        "Market :",
        mc_stage(r["mc"])
    )


    print(
        "Highest MC :",
        r["mc"]
    )


    print(
        "Category :",
        category(
            r["score"],
            r["mc"]
        )
    )


    print(
        "Signals :",
        r["signals"]
    )


    print(
        "Missing :",
        r["missing"]
    )


    print("------------------------------")


    rank+=1