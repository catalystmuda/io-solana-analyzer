import sqlite3
import time
import requests

DB = "backend/database/tokens.db"


def update_token(mint):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    row = conn.execute("""
    SELECT id
    FROM tokens
    WHERE mint=?
    """, (mint,)).fetchone()

    if not row:
        conn.close()
        return False

    url = f"https://api.dexscreener.com/latest/dex/tokens/{mint}"

    # tunggu pair benar-benar matang
    for attempt in range(20):

        try:

            r = requests.get(url, timeout=10)

            if r.status_code != 200:
                time.sleep(3)
                continue

            data = r.json()

            pairs = data.get("pairs")

            if not pairs:
                print(f"[{attempt+1}/20] Pair belum ada...")
                time.sleep(3)
                continue

            # pilih pair dengan volume terbesar
            pair = max(
                pairs,
                key=lambda p: (
                    p.get("volume", {}).get("h24", 0) or 0
                )
            )

            liquidity = pair.get("liquidity", {}).get("usd", 0) or 0
            volume24 = pair.get("volume", {}).get("h24", 0) or 0
            fdv = pair.get("fdv", 0) or 0
            price = pair.get("priceUsd", 0) or 0

            conn.execute("""
            UPDATE tokens
            SET
                pair_address=?,
                dex=?,
                chain=?,
                liquidity=?,
                volume24=?,
                fdv=?,
                price_usd=?,
                last_update=datetime('now')
            WHERE id=?
            """,
            (
                pair.get("pairAddress"),
                pair.get("dexId"),
                pair.get("chainId"),
                liquidity,
                volume24,
                fdv,
                price,
                row["id"]
            ))

            conn.commit()

            print("=" * 70)
            print("DEX READY")
            print("=" * 70)
            print("PAIR :", pair.get("pairAddress"))
            print("DEX  :", pair.get("dexId"))
            print("CHAIN:", pair.get("chainId"))
            print("PRICE:", price)
            print("LIQ  :", liquidity)
            print("VOL24:", volume24)
            print("FDV  :", fdv)
            print("=" * 70)

            conn.close()
            return True

        except Exception:
            time.sleep(3)

    conn.close()

    print("=" * 70)
    print("DEX TIMEOUT")
    print(mint)
    print("=" * 70)

    return False


def update_all(limit=300):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
    SELECT mint
    FROM tokens
    ORDER BY id DESC
    LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    updated = 0

    for row in rows:

        if update_token(row["mint"]):
            updated += 1

    print("=" * 70)
    print("UPDATED :", updated)
    print("=" * 70)


if __name__ == "__main__":

    update_all()