import sqlite3
import os

DB = os.path.join("backend", "database", "tokens.db")

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
SELECT
t.name,
t.symbol,
t.market_cap_sol,
t.sol_amount,
c.reputation_score,
c.category
FROM tokens t
LEFT JOIN creator_memory c
ON t.creator=c.creator
ORDER BY t.created_at DESC
LIMIT 200
""")

print("="*70)
print("FINAL ALPHA SCORE V2")
print("="*70)

for r in cur.fetchall():

    score = 0

    mc = r["market_cap_sol"] or 0
    buy = r["sol_amount"] or 0
    rep = r["reputation_score"] or 0

    if mc >= 50:
        score += 20

    if mc >= 100:
        score += 30

    if buy >= 10:
        score += 10

    if buy >= 20:
        score += 20

    score += rep

    # tampilkan hanya token layak
    if score < 60:
        continue

    print()
    print(r["name"])
    print("SYMBOL :", r["symbol"])
    print("MC     :", round(mc,2))
    print("BUY    :", round(buy,2))
    print("REP    :", rep)
    print("SCORE  :", score)

    if score >= 90:
        print("🔥 STRONG BUY")
    elif score >= 75:
        print("✅ WATCH")
    else:
        print("👀 OBSERVE")

conn.close()