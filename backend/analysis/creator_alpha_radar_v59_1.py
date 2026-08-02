import sqlite3


DB = "backend/database/tokens.db"


print("==============================")
print(" CREATOR ALPHA RADAR V59.1 ")
print(" SCORE NORMALIZER ENGINE ")
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
    market_cap_sol
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





def market_stage(mc):


    if mc >=1000:
        return "BREAKOUT"


    elif mc>=300:
        return "MOMENTUM"


    elif mc>=100:
        return "EARLY"


    elif mc>=50:
        return "GENESIS"


    return "DEAD"





def confidence(score):


    if score>=85:
        return "VERY HIGH"


    elif score>=70:
        return "HIGH"


    elif score>=50:
        return "MEDIUM"


    return "LOW"





def risk(score,market):


    if score>=80 and market in ["BREAKOUT","MOMENTUM"]:

        return "LOW"



    if score>=50:

        return "MEDIUM"



    return "HIGH"






def entry_status(market,score):


    if market=="EARLY" and score>=70:

        return "EARLY ENTRY"


    if market=="MOMENTUM" and score>=80:

        return "MOMENTUM ENTRY"


    if market=="BREAKOUT":

        return "BREAKOUT FOLLOW"


    return "WATCH"







def analyze(token,creator_db):


    mint=token[1]
    name=token[2]
    symbol=token[3]
    creator=token[4]
    mc=token[5] or 0


    raw=0


    signals=[]



    if creator in creator_db:


        c=creator_db[creator]


        total=c[1]
        breakout=c[3]
        survivor=c[4]
        reputation=c[5]



        if survivor>0:

            raw+=25
            signals.append("SURVIVOR")



        if breakout>0:

            raw+=25
            signals.append("BREAKOUT HISTORY")



        if reputation>=70:

            raw+=25
            signals.append("REPUTATION")



        if total<=3:

            raw+=10
            signals.append("LOW TOKEN CREATOR")




    market=market_stage(mc)



    if market=="EARLY":

        raw+=10
        signals.append("EARLY MC")



    elif market=="MOMENTUM":

        raw+=15
        signals.append("MOMENTUM")



    elif market=="BREAKOUT":

        raw+=15
        signals.append("BREAKOUT")




    if raw>100:

        raw=100



    return {

        "mint":mint,
        "name":name,
        "symbol":symbol,
        "creator":creator,
        "score":raw,
        "market":market,
        "confidence":confidence(raw),
        "risk":risk(raw,market),
        "entry":entry_status(market,raw),
        "signals":signals

    }





tokens=load_tokens()

creator_db=load_creator_memory()



results=[]


for t in tokens:


    results.append(
        analyze(t,creator_db)
    )



results=sorted(
    results,
    key=lambda x:x["score"],
    reverse=True
)



print()

print("TOTAL TOKENS :",len(results))


found=0



for r in results:


    if r["score"] <50:

        continue


    found+=1


    print()

    print("#",found)

    print("Token :",r["name"])
    print("Symbol :",r["symbol"])
    print("Mint :",r["mint"])

    print("Creator :",r["creator"])

    print("Alpha Score :",r["score"],"%")

    print("Confidence :",r["confidence"])

    print("Risk Level :",r["risk"])

    print("Entry :",r["entry"])

    print("Market :",r["market"])

    print("Signals :",r["signals"])

    print("------------------------------")



    if found>=30:

        break



print()

print("FOUND :",found)