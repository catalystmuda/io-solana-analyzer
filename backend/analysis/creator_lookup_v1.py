import sqlite3

DB = "backend/database/tokens.db"

creator = input("Creator : ").strip()

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
SELECT
name,
symbol,
market_cap_sol,
sol_amount,
created_at
FROM tokens
WHERE creator=?
ORDER BY created_at DESC
""", (creator,))

rows = cur.fetchall()

print("=" * 60)
print("TOTAL TOKEN :", len(rows))
print("=" * 60)

for i, r in enumerate(rows, 1):
    print(f"\n#{i}")
    print("TOKEN :", r["name"])
    print("SYMBOL:", r["symbol"])
    print("MC    :", round(r["market_cap_sol"] or 0, 2))
    print("BUY   :", round(r["sol_amount"] or 0, 2))
    print("TIME  :", r["created_at"])

conn.close()