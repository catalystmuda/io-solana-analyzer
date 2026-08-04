import sqlite3
import requests
import time

DB = "backend/database/tokens.db"


def update_one(signal):

    mint = signal["mint"]

    try:

        url = f"https://api.dexscreener.com/latest/dex/tokens/{mint}"

        r = requests.get(url, timeout=15)

        if r.status_code != 200:
            return

        data = r.json()

        pairs = data.get("pairs")

        if not pairs:
            return

        pair = max(
            pairs,
            key=lambda p: (
                p.get("volume", {}).get("h24", 0) or 0
            )
        )

        current_fdv = pair.get("fdv", 0) or 0
        current_volume = pair.get("volume", {}).get("h24", 0) or 0
        current_liquidity = pair.get("liquidity", {}).get("usd", 0) or 0
        current_price = float(pair.get("priceUsd", 0) or 0)

        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row

        row = conn.execute("""
        SELECT
            fdv
        FROM elite_signals
        WHERE mint=?
        """, (mint,)).fetchone()

        if row is None:
            conn.close()
            return

        start_fdv = row["fdv"] or 0

        roi = 0

        if start_fdv > 0:
            roi = ((current_fdv - start_fdv) / start_fdv) * 100

        conn.execute("""
        UPDATE elite_signals
        SET
            current_fdv=?,
            current_volume=?,
            current_liquidity=?,
            current_price=?,
            roi=?,
            last_checked=datetime('now')
        WHERE mint=?
        """,
        (
            current_fdv,
            current_volume,
            current_liquidity,
            current_price,
            roi,
            mint
        ))

        conn.commit()
        conn.close()

        print("=" * 70)
        print(signal["symbol"])
        print("FDV :", start_fdv, "->", current_fdv)
        print("ROI :", round(roi, 2), "%")
        print("=" * 70)

    except Exception as e:

        print(e)


def worker():

    print("=" * 70)
    print("PAPER TRADE WORKER")
    print("=" * 70)

    while True:

        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
        SELECT *
        FROM elite_signals
        ORDER BY id DESC
        """).fetchall()

        conn.close()

        for row in rows:

            update_one(row)

            time.sleep(1)

        time.sleep(300)


if __name__ == "__main__":

    worker()