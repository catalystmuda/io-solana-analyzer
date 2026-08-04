import sqlite3
import requests
import time

DB = "backend/database/tokens.db"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

rows = conn.execute("""
SELECT id,mint
FROM tokens
WHERE pair_address IS NULL
ORDER BY id DESC
LIMIT 300
""").fetchall()

print("=" * 70)
print("DEXSCREENER UPDATER")
print("=" * 70)

updated = 0

for row in rows:

    mint = row["mint"]

    try:

        url = f"https://api.dexscreener.com/latest/dex/tokens/{mint}"

        r = requests.get(url, timeout=15)

        if r.status_code != 200:
            continue

        data = r.json()

        pairs = data.get("pairs")

        if not pairs:
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
        WHERE id=?
        """,(
            pair.get("pairAddress"),
            pair.get("dexId"),
            pair.get("chainId"),
            pair.get("liquidity",{}).get("usd",0),
            pair.get("volume",{}).get("h24",0),
            pair.get("fdv",0),
            pair.get("priceUsd",0),
            row["id"]
        ))

        conn.commit()

        updated += 1

        print("UPDATED :", mint)

    except Exception:
        pass

    time.sleep(0.25)

print("=" * 70)
print("UPDATED :", updated)
print("=" * 70)

conn.close()