import sqlite3


DB = "backend/database/tokens.db"


def calculate_category(roi):
    if roi >= 500:
        return "ALPHA"
    elif roi >= 100:
        return "WINNER"
    elif roi >= 0:
        return "NORMAL"
    else:
        return "LOSER"


def main():

    print("==============================")
    print(" WALLET ROI ENGINE V1 ")
    print("==============================")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            wallet,
            token_symbol,
            entry_mc,
            exit_mc
        FROM wallet_activity
    """)

    rows = cur.fetchall()

    print("\nTOTAL ACTIVITY :", len(rows))

    results = {}

    for wallet, symbol, entry_mc, exit_mc in rows:

        if entry_mc is None or entry_mc == 0:
            continue

        peak_mc = exit_mc if exit_mc and exit_mc > 0 else entry_mc

        roi = ((peak_mc - entry_mc) / entry_mc) * 100

        if wallet not in results:
            results[wallet] = {
                "trades": 0,
                "best_roi": roi,
                "best_token": symbol
            }

        results[wallet]["trades"] += 1

        if roi > results[wallet]["best_roi"]:
            results[wallet]["best_roi"] = roi
            results[wallet]["best_token"] = symbol


    ranked = sorted(
        results.items(),
        key=lambda x: x[1]["best_roi"],
        reverse=True
    )


    print("\nTOTAL WALLETS :", len(ranked))

    for i, (wallet, data) in enumerate(ranked[:20], 1):

        category = calculate_category(data["best_roi"])

        print("------------------------------")
        print("#", i)
        print("Wallet :", wallet)
        print("Trades :", data["trades"])
        print("Best Token :", data["best_token"])
        print("ROI :", round(data["best_roi"],2), "%")
        print("Category :", category)


    conn.close()


if __name__ == "__main__":
    main()