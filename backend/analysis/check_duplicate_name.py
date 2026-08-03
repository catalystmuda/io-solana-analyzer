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
COUNT(*) total
FROM tokens
GROUP BY name,symbol
HAVING COUNT(*)>1
ORDER BY total DESC
""")

for r in cur.fetchall():

    print("="*60)
    print(r["name"])
    print(r["symbol"])
    print("TOTAL :", r["total"])

conn.close()