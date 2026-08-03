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
SELECT *
FROM tokens
ORDER BY id DESC
LIMIT 500
""")

rows = cur.fetchall()

best = {}

for r in rows:

    mint = r["mint"]

    if mint not in best:
        best[mint] = r
        continue

    if r["market_cap_sol"] > best[mint]["market_cap_sol"]:
        best[mint] = r

print("=" * 70)
print("FINAL ALPHA SCORE V8")
print("=" * 70)

for r in best.values():

    cur.execute("""
    SELECT *
    FROM creator_memory
    WHERE creator=?
    """, (r["creator"],))

    mem = cur.fetchone()

    if mem is None:
        continue

    rep = mem["reputation_score"]
    risk = mem["risk_score"]
    breakout = mem["breakout_count"]
    survivor = mem["survivor_count"]

    mc = r["market_cap_sol"] or 0
    buy = r["sol_amount"] or 0

    score = (
        rep
        + mc/5
        + buy
        + breakout*20
        + survivor*5
        - risk
    )

    if score < 100:
        continue

    print()
    print(r["name"])
    print("SYMBOL :", r["symbol"])
    print("MC     :", round(mc,2))
    print("BUY    :", round(buy,2))
    print("FINAL  :", round(score,2))

conn.close()