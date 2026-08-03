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
LIMIT 300
""")

rows = cur.fetchall()

print("="*70)
print("FINAL ALPHA SCORE V3")
print("="*70)

for r in rows:

    creator = r["creator"]

    cur.execute("""
    SELECT reputation_score,risk_score,category
    FROM creator_memory
    WHERE creator=?
    """,(creator,))

    mem = cur.fetchone()

    if not mem:
        continue

    rep = mem["reputation_score"]
    risk = mem["risk_score"]

    mc = r["market_cap_sol"] or 0
    buy = r["initial_buy"] or 0

    score = (
        rep
        + mc/4
        + buy*2
        - risk
    )

    if rep < 50:
        continue

    if mc < 100:
        continue

    if buy < 20:
        continue

    print()
    print(r["name"])
    print("SYMBOL :",r["symbol"])
    print("MC     :",round(mc,2))
    print("BUY    :",round(buy,2))
    print("REP    :",rep)
    print("RISK   :",risk)
    print("SCORE  :",round(score,2))

    if score>=120:
        print("🔥 ELITE ENTRY")

    elif score>=80:
        print("✅ GOOD")

    else:
        print("👀 WATCH")

conn.close()