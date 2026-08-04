from backend.analysis.dex_updater import update_token
from backend.analysis.alpha_score_v11 import calculate_score
from backend.analysis.recommendation_engine import check_token

import sqlite3

DB = "backend/database/tokens.db"


def early_alpha(payload):

    score = 0

    marketcap = payload.get("marketCapSol", 0)
    initial_buy = payload.get("initialBuy", 0)
    sol_amount = payload.get("solAmount", 0)
    vsol = payload.get("vSolInBondingCurve", 0)

    # =====================================
    # EARLY MARKETCAP
    # =====================================

    if 20 <= marketcap <= 80:
        score += 80

    elif 80 < marketcap <= 200:
        score += 50

    else:
        score -= 30

    # =====================================
    # INITIAL BUY
    # =====================================

    if initial_buy > 50000000:
        score += 120

    elif initial_buy > 10000000:
        score += 60

    # =====================================
    # SOL INVESTED
    # =====================================

    if sol_amount >= 2:
        score += 100

    elif sol_amount >= 1:
        score += 50

    # =====================================
    # BONDING CURVE
    # =====================================

    if vsol >= 30:
        score += 50

    return round(score, 2)


def save_payload(payload):

    conn = sqlite3.connect(DB)

    conn.execute(
        """
        INSERT INTO tokens
        (
            mint,
            name,
            symbol,
            creator,
            market_cap_sol,
            uri,
            created_at
        )
        VALUES
        (
            ?,?,?,?,?,?,datetime('now')
        )

        ON CONFLICT(mint)
        DO UPDATE SET

            name=excluded.name,
            symbol=excluded.symbol,
            creator=excluded.creator,
            market_cap_sol=excluded.market_cap_sol,
            uri=excluded.uri
        """,
        (
            payload["mint"],
            payload.get("name"),
            payload.get("symbol"),
            payload.get("traderPublicKey"),
            payload.get("marketCapSol", 0),
            payload.get("uri"),
        ),
    )

    conn.commit()
    conn.close()


def process_token(payload):

    mint = payload["mint"]

    print("=" * 70)
    print("PROCESS :", mint)
    print("=" * 70)

    early = early_alpha(payload)

    print("EARLY ALPHA :", early)

    save_payload(payload)

    ok = update_token(mint)

    if not ok:

        print("=" * 70)
        print("TOKEN SAVED")
        print("WAITING FOR RECHECK WORKER")
        print("=" * 70)

        return

    final_score = calculate_score(mint)

    if final_score is None:

        print("WAITING MARKET DATA")
        return

    print("=" * 70)
    print("FINAL ALPHA :", final_score)
    print("=" * 70)

    check_token(mint, final_score)


if __name__ == "__main__":

    print("Use live_listener.py")