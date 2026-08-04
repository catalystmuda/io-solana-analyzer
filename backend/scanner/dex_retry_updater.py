import sqlite3
import time
import requests

DB = "backend/database/tokens.db"


def update_dex_until_ready(mint, retry=15, delay=5):

    conn = sqlite3.connect(DB)

    for i in range(retry):

        try:

            url = f"https://api.dexscreener.com/latest/dex/tokens/{mint}"

            r = requests.get(url, timeout=15)

            if r.status_code != 200:

                print(f"[{i+1}/{retry}] HTTP {r.status_code}")

                time.sleep(delay)

                continue

            data = r.json()

            pairs = data.get("pairs")

            if not pairs:

                print(f"[{i+1}/{retry}] Pair belum ada...")

                time.sleep(delay)

                continue

            pair = pairs[0]

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
            WHERE mint=?
            """,(
                pair.get("pairAddress"),
                pair.get("dexId"),
                pair.get("chainId"),
                pair.get("liquidity", {}).get("usd", 0),
                pair.get("volume", {}).get("h24", 0),
                pair.get("fdv", 0),
                pair.get("priceUsd", 0),
                mint
            ))

            conn.commit()
            conn.close()

            print("=" * 70)
            print("DEX READY")
            print("=" * 70)
            print("PAIR :", pair.get("pairAddress"))
            print("DEX  :", pair.get("dexId"))
            print("CHAIN:", pair.get("chainId"))
            print("PRICE:", pair.get("priceUsd"))
            print("LIQ  :", pair.get("liquidity", {}).get("usd", 0))
            print("VOL24:", pair.get("volume", {}).get("h24", 0))
            print("FDV  :", pair.get("fdv", 0))
            print("=" * 70)

            return True

        except Exception as e:

            print("ERROR :", e)

        time.sleep(delay)

    conn.close()

    print("=" * 70)
    print("DEX TIMEOUT")
    print(mint)
    print("=" * 70)

    return False