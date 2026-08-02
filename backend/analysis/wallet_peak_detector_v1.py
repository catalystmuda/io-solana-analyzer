import sqlite3


DB = "backend/database/tokens.db"


def main():

    print("==============================")
    print(" WALLET PEAK DETECTOR V1 ")
    print("==============================")


    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.execute("""
        SELECT
            w.wallet,
            w.token_symbol,
            w.entry_mc,
            MAX(t.market_cap_sol)
        FROM wallet_activity w
        JOIN tokens t
        ON w.token_mint = t.mint
        GROUP BY w.wallet, w.token_mint
        ORDER BY MAX(t.market_cap_sol) DESC
        LIMIT 20
    """)


    rows = cur.fetchall()


    print("TOTAL RESULTS :", len(rows))


    for i,row in enumerate(rows,1):

        wallet, symbol, entry, peak = row

        if entry:
            roi = ((peak-entry)/entry)*100
        else:
            roi = 0


        print("------------------------------")
        print("#",i)
        print("Wallet :",wallet)
        print("Token :",symbol)
        print("Entry MC :",entry)
        print("Peak MC :",peak)
        print("ROI :",round(roi,2),"%")


    conn.close()



if __name__ == "__main__":
    main()