import sqlite3
import requests
import time

DB = "backend/database/tokens.db"


def get_latest(mint):

    try:

        url = f"https://api.dexscreener.com/latest/dex/tokens/{mint}"

        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return None

        data = r.json()

        pairs = data.get("pairs")

        if not pairs:
            return None

        pair = max(
            pairs,
            key=lambda p: p.get("volume", {}).get("h24", 0) or 0
        )

        return {

            "fdv": pair.get("fdv", 0) or 0,
            "price": float(pair.get("priceUsd", 0) or 0),
            "volume": pair.get("volume", {}).get("h24", 0) or 0,
            "liquidity": pair.get("liquidity", {}).get("usd", 0) or 0,

        }

    except:

        return None


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

        WHERE status='OPEN'

        ORDER BY id DESC

        """).fetchall()

        for row in rows:

            latest = get_latest(row["mint"])

            if latest is None:
                continue

            start_fdv = row["fdv"] or 0

            current_fdv = latest["fdv"]

            ath_fdv = max(row["ath_fdv"] or 0, current_fdv)

            roi = 0

            if start_fdv > 0:
                roi = ((current_fdv - start_fdv) / start_fdv) * 100

            conn.execute("""

            UPDATE elite_signals

            SET

                current_fdv=?,

                ath_fdv=?,

                current_price=?,

                roi=?,

                last_checked=datetime('now')

            WHERE id=?

            """,

            (

                current_fdv,

                ath_fdv,

                latest["price"],

                roi,

                row["id"]

            ))

            conn.commit()

            print("=" * 70)
            print(row["symbol"])
            print("ALPHA :", row["alpha_score"])
            print("ENTRY :", round(start_fdv, 2))
            print("NOW   :", round(current_fdv, 2))
            print("ATH   :", round(ath_fdv, 2))
            print("ROI   :", round(roi, 2), "%")
            print("=" * 70)

            time.sleep(1)

        conn.close()

        time.sleep(60)


if __name__ == "__main__":

    worker()