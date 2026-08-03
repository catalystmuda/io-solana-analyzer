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
id,
name,
symbol,
creator,
market_cap_sol,
sol_amount
FROM tokens
WHERE symbol='SAOF'
ORDER BY id DESC
""")

for r in cur.fetchall():

    print("="*60)
    print("ID      :", r["id"])
    print("NAME    :", r["name"])
    print("CREATOR :", r["creator"])
    print("MC      :", r["market_cap_sol"])
    print("BUY     :", r["sol_amount"])

conn.close()