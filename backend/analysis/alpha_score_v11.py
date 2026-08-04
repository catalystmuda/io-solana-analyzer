import sqlite3

DB = "backend/database/tokens.db"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

rows = conn.execute("""
SELECT *
FROM tokens
WHERE liquidity > 0
ORDER BY liquidity DESC
""").fetchall()

print("=" * 70)
print("IO SOLANA ANALYZER v1.1")
print("=" * 70)

shown_creator = set()

for row in rows:

    creator = row["creator"]

    if creator in shown_creator:
        continue

    shown_creator.add(creator)

    memory = conn.execute("""
    SELECT *
    FROM creator_memory
    WHERE creator=?
    """, (creator,)).fetchone()

    if memory is None:
        continue

    category = memory["category"]

    if category == "ELITE":
        bonus = 150

    elif category == "GOOD":
        bonus = 75

    elif category == "NORMAL":
        bonus = 25

    else:
        bonus = 0

    score = (
        memory["reputation_score"] * 3
        + memory["breakout_count"] * 100
        + memory["survivor_count"] * 30
        + row["market_cap_sol"] * 0.30
        + row["liquidity"] * 0.002
        + row["volume24"] * 0.001
        + bonus
    )

    print()
    print("NAME      :", row["name"])
    print("SYMBOL    :", row["symbol"])
    print("CATEGORY  :", category)
    print("MC SOL    :", round(row["market_cap_sol"], 2))
    print("FDV USD   :", round(row["fdv"], 2))
    print("LIQUIDITY :", round(row["liquidity"], 2))
    print("VOLUME24  :", round(row["volume24"], 2))
    print("REP       :", memory["reputation_score"])
    print("BREAKOUT  :", memory["breakout_count"])
    print("SURVIVOR  :", memory["survivor_count"])
    print("FINAL     :", round(score, 2))

conn.close()