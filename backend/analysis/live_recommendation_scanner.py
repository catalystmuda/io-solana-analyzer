import sqlite3
import time

DB = "backend/database/tokens.db"

shown = set()

print("=" * 70)
print("IO SOLANA ANALYZER")
print("LIVE RECOMMENDATION SCANNER")
print("=" * 70)

while True:

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
    SELECT
        t.mint,
        t.name,
        t.symbol,
        t.creator,
        t.liquidity,
        t.volume24,
        t.fdv,
        c.category,
        c.reputation_score,
        c.breakout_count,
        c.survivor_count
    FROM tokens t
    LEFT JOIN creator_memory c
    ON t.creator=c.creator
    ORDER BY t.created_at DESC
    LIMIT 100
    """).fetchall()

    conn.close()

    for row in rows:

        mint = row["mint"]

        if mint in shown:
            continue

        liquidity = row["liquidity"] or 0
        volume = row["volume24"] or 0
        fdv = row["fdv"] or 0
        rep = row["reputation_score"] or 0
        breakout = row["breakout_count"] or 0
        survivor = row["survivor_count"] or 0
        category = row["category"] or "RISK"

        if liquidity < 5000:
            continue

        if volume < 5000:
            continue

        if fdv < 100000:
            continue

        if rep < 20:
            continue

        score = 0

        score += rep * 5
        score += breakout * 50
        score += survivor * 20
        score += liquidity / 1000
        score += volume / 1000
        score += fdv / 100000

        if category == "ELITE":
            score += 300

        print()
        print("=" * 70)
        print("🔥 NEW RECOMMENDED TOKEN")
        print("=" * 70)
        print("NAME      :", row["name"])
        print("SYMBOL    :", row["symbol"])
        print("CA        :", mint)
        print("CATEGORY  :", category)
        print("SCORE     :", round(score, 2))
        print("LIQUIDITY :", round(liquidity, 2))
        print("VOLUME24  :", round(volume, 2))
        print("FDV       :", round(fdv, 2))
        print("=" * 70)

        shown.add(mint)

    time.sleep(15)