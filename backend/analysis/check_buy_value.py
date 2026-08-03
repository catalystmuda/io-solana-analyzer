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
name,
symbol,
initial_buy,
sol_amount,
market_cap_sol
FROM tokens
ORDER BY id DESC
LIMIT 20
""")

for r in cur.fetchall():

    print("="*50)
    print(r["name"])
    print("initial_buy :", r["initial_buy"])
    print("sol_amount  :", r["sol_amount"])
    print("mc          :", r["market_cap_sol"])

conn.close()