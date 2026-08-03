import sqlite3
import os

DB = os.path.join(
    "backend",
    "database",
    "tokens.db"
)

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
LIMIT 50
""")

print("="*70)
print("FINAL ALPHA SCORE")
print("="*70)

for r in cur.fetchall():

    score = 0

    if r["market_cap_sol"] >= 100:
        score += 30
    elif r["market_cap_sol"] >= 50:
        score += 20

    if r["sol_amount"] >= 20:
        score += 20
    elif r["sol_amount"] >= 10:
        score += 10

    score += min(r["reputation_score"] or 0, 50)

    if score >= 80:
        signal = "🔥 STRONG BUY"
    elif score >= 60:
        signal = "✅ WATCH"
    else:
        signal = "❌ SKIP"

    print()
    print(r["name"])
    print("Score :", score)
    print(signal)

conn.close()