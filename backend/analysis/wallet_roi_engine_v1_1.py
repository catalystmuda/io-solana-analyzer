import sqlite3


DB = "backend/database/tokens.db"


def category(roi):
    if roi >= 500:
        return "ALPHA"
    elif roi >= 100:
        return "WINNER"
    elif roi > 0:
        return "PROFIT"
    else:
        return "NO DATA"


def main():

    print("==============================")
    print(" WALLET ROI ENGINE V1.1 ")
    print(" MC LINKED MODE ")
    print("==============================")


    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
        SELECT
            w.wallet,
            w.token_symbol,
            w.entry_mc,
            t.market_cap_sol
        FROM wallet_activity w
        LEFT JOIN tokens t
        ON w.token_mint = t.mint
    """)


    rows = cur.fetchall()


    wallets = {}


    for wallet, symbol, entry_mc, current_mc in rows:

        if not entry_mc or not current_mc:
            continue


        roi = ((current_mc - entry_mc) / entry_mc) * 100


        if wallet not in wallets:
            wallets[wallet] = {
                "trades": 0,
                "best_roi": roi,
                "token": symbol,
                "mc": current_mc
            }


        wallets[wallet]["trades"] += 1


        if roi > wallets[wallet]["best_roi"]:
            wallets[wallet]["best_roi"] = roi
            wallets[wallet]["token"] = symbol
            wallets[wallet]["mc"] = current_mc



    ranking = sorted(
        wallets.items(),
        key=lambda x: x[1]["best_roi"],
        reverse=True
    )


    print("\nTOTAL WALLET :", len(ranking))


    for i,(wallet,data) in enumerate(ranking[:20],1):

        print("------------------------------")
        print("#",i)
        print("Wallet :",wallet)
        print("Trades :",data["trades"])
        print("Best Token :",data["token"])
        print("Peak MC :",round(data["mc"],2))
        print("ROI :",round(data["best_roi"],2),"%")
        print("Category :",category(data["best_roi"]))


    conn.close()



if __name__ == "__main__":
    main()