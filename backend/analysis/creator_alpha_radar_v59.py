import sqlite3
from datetime import datetime


DB = "backend/database/tokens.db"


print("==============================")
print(" CREATOR ALPHA RADAR V59 ")
print(" TOKEN EARLY ALPHA ENGINE ")
print("==============================")


def load_tokens():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT
    id,
    mint,
    name,
    symbol,
    creator,
    market_cap_sol,
    created_at
    FROM tokens
    """)

    rows = cur.fetchall()

    conn.close()

    return rows



def load_creator_memory():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT
    creator,
    total_tokens,
    highest_mc,
    breakout_count,
    survivor_count,
    reputation_score
    FROM creator_memory
    """)

    rows = cur.fetchall()

    conn.close()

    data={}

    for r in rows:

        data[r[0]]=r

    return data




def mc_stage(mc):

    if mc >=1000:
        return "BREAKOUT"

    elif mc>=300:
        return "MOMENTUM"

    elif mc>=100:
        return "EARLY"

    elif mc>=50:
        return "GENESIS"

    return "DEAD"





def analyze_token(token,creator_db):


    mint=token[1]
    name=token[2]
    symbol=token[3]
    creator=token[4]
    mc=token[5] or 0


    score=0

    signals=[]

    missing=[]


    market=mc_stage(mc)



    # creator quality

    if creator in creator_db:


        c=creator_db[creator]

        total=c[1]
        highest=c[2]
        breakout=c[3]
        survivor=c[4]
        reputation=c[5]


        if survivor>0:
            score+=30
            signals.append("GOOD CREATOR")


        if breakout>0:
            score+=25
            signals.append("BREAKOUT HISTORY")


        if reputation>=70:
            score+=20
            signals.append("REPUTATION")



        if total<=3:
            score+=10
            signals.append("LOW SUPPLY CREATOR")

        else:
            missing.append("MANY TOKENS")


    else:

        missing.append("UNKNOWN CREATOR")




    # market


    if market=="EARLY":

        score+=15
        signals.append("EARLY MC")


    elif market=="MOMENTUM":

        score+=25
        signals.append("MOMENTUM")

    elif market=="BREAKOUT":

        score+=20
        signals.append("BREAKOUT")



    if score>=80:

        opportunity="ALPHA CANDIDATE"


    elif score>=60:

        opportunity="WATCH"


    else:

        opportunity="IGNORE"



    return {

        "mint":mint,
        "name":name,
        "symbol":symbol,
        "creator":creator,
        "score":score,
        "opportunity":opportunity,
        "market":market,
        "signals":signals,
        "missing":missing

    }






tokens=load_tokens()

creators=load_creator_memory()


results=[]


for t in tokens:

    results.append(
        analyze_token(t,creators)
    )



results=sorted(
    results,
    key=lambda x:x["score"],
    reverse=True
)



print()

print("TOTAL TOKENS :",len(results))


count=0


for r in results:


    if r["opportunity"]=="IGNORE":
        continue


    count+=1


    print()

    print("#",count)

    print("Token :",r["name"])
    print("Symbol :",r["symbol"])
    print("Mint :",r["mint"])

    print("Creator :",r["creator"])

    print("Alpha Score :",r["score"])

    print("Opportunity :",r["opportunity"])

    print("Market :",r["market"])

    print("Signals :",r["signals"])

    print("Missing :",r["missing"])

    print("------------------------------")


    if count>=30:
        break



print()

print("FOUND :",count)