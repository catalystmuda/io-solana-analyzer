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
t.creator,
c.category,
c.reputation_score,
c.risk_score
FROM tokens t
LEFT JOIN creator_memory c
ON t.creator=c.creator
ORDER BY t.created_at DESC
LIMIT 50
""")

rows = cur.fetchall()

print("="*70)
print("FINAL ENTRY FILTER")
print("="*70)

for r in rows:

    if r["category"] == "RISK":
        continue

    print()
    print(r["name"])
    print("SYMBOL :", r["symbol"])
    print("MC     :", round(r["market_cap_sol"],2))
    print("BUY    :", round(r["sol_amount"],2))
    print("REP    :", r["reputation_score"])
    print("RISK   :", r["risk_score"])
    print("TYPE   :", r["category"])

conn.close()