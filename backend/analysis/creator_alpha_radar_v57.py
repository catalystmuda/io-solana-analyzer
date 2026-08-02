import json
import os


print("==============================")
print(" CREATOR ALPHA RADAR V57 ")
print(" EARLY SIGNAL ENGINE ")
print("==============================\n")


DATA_FILE = "data/creator_history.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE,"r") as f:
        return json.load(f)



def analyze_creator(c):

    tokens = c.get("tokens",1)
    mc = c.get("highest_mc",0)

    survivor = c.get("survivor",False)
    breakout = c.get("breakout",False)

    reputation = c.get("reputation",0)


    score = 0
    signals=[]
    missing=[]


    # survivor
    if survivor:
        score +=25
        signals.append("SURVIVOR")
    else:
        missing.append("NO SURVIVOR")


    # breakout
    if breakout:
        score +=30
        signals.append("BREAKOUT")
    else:
        missing.append("NO BREAKOUT")


    # market cap
    if mc >=1000:
        score +=25
        signals.append("ELITE MC")

    elif mc >=300:
        score +=15
        signals.append("MC 300+")

    elif mc >=100:
        score +=8
        signals.append("EARLY MC")

    else:
        missing.append("LOW MC")



    # creator quality
    if reputation >=80:
        score +=20
        signals.append("REPUTATION")

    elif reputation >=50:
        score +=10
        signals.append("CREATOR HISTORY")


    # hidden alpha
    if survivor and mc <300 and not breakout:
        score +=10
        signals.append("HIDDEN ALPHA")


    # spam filter

    risk="LOW"

    if tokens >20:
        score -=40
        risk="HIGH"
        missing.append("MANY TOKENS")


    if tokens >5:
        score -=20
        risk="MEDIUM"



    score=max(score,0)

    probability=min(score,100)



    if score >=80:
        opportunity="ELITE ALPHA"

    elif score >=55:
        opportunity="EARLY WATCH"

    elif score >=30:
        opportunity="SPECULATIVE"

    else:
        opportunity="UNKNOWN"



    if breakout and reputation>=80:
        dna="ALPHA CREATOR"

    elif survivor and mc>=300:
        dna="MOMENTUM GEM"

    elif survivor:
        dna="EARLY GEM"

    else:
        dna="GENESIS"



    return {
        "creator":c.get("creator"),
        "Hunter Score":score,
        "Alpha Probability":probability,
        "Opportunity":opportunity,
        "Risk Level":risk,
        "Tokens":tokens,
        "Market":c.get("market","UNKNOWN"),
        "Highest MC":mc,
        "DNA":dna,
        "Signals":signals,
        "Missing":missing
    }




data=load_data()


results=[]

for c in data:
    results.append(analyze_creator(c))


results.sort(
    key=lambda x:x["Hunter Score"],
    reverse=True
)


print("TOTAL :",len(results))
print()


for i,r in enumerate(results[:50],1):

    print("#",i)
    print("Creator :",r["creator"])
    print("Hunter Score :",r["Hunter Score"])
    print("Alpha Probability :",r["Alpha Probability"],"%")
    print("Opportunity :",r["Opportunity"])
    print("Risk Level :",r["Risk Level"])
    print("Tokens :",r["Tokens"])
    print("Market :",r["Market"])
    print("Highest MC :",r["Highest MC"])
    print("DNA :",r["DNA"])
    print("Signals :",r["Signals"])
    print("Missing :",r["Missing"])
    print("-"*30)