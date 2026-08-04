import sqlite3
import threading
import time

from backend.analysis.dex_updater import update_token
from backend.analysis.alpha_score_v11 import calculate_score
from backend.analysis.recommendation_engine import check_token

DB = "backend/database/tokens.db"


def recheck_after_delay(mint, delay=60):

    print("=" * 70)
    print("RECHECK QUEUED :", mint)
    print("WAIT :", delay, "SECONDS")
    print("=" * 70)

    time.sleep(delay)

    print("=" * 70)
    print("RECHECK :", mint)
    print("=" * 70)

    ok = update_token(mint)

    if not ok:
        print("Dex update failed")
        return

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    row = conn.execute("""
    SELECT
        liquidity,
        volume24,
        fdv
    FROM tokens
    WHERE mint=?
    """, (mint,)).fetchone()

    conn.close()

    if row is None:
        return

    liq = row["liquidity"] or 0
    vol = row["volume24"] or 0
    fdv = row["fdv"] or 0

    print("LIQ :", liq)
    print("VOL :", vol)
    print("FDV :", fdv)

    if liq < 5000 and vol < 5000 and fdv < 100000:
        print("Not enough quality")
        return

    score = calculate_score(mint)

    print("=" * 70)
    print("ALPHA :", round(score, 2))
    print("=" * 70)

    check_token(mint, score)


def add_to_queue(mint, delay=60):

    thread = threading.Thread(
        target=recheck_after_delay,
        args=(mint, delay),
        daemon=True
    )

    thread.start()