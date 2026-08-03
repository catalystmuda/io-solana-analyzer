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
mint,
COUNT(*) total
FROM tokens
GROUP BY mint
HAVING COUNT(*)>1
ORDER BY total DESC
""")

for r in cur.fetchall():

    print("="*60)
    print("MINT :", r["mint"])
    print("TOTAL:", r["total"])

    cur.execute("""
    SELECT
    id,
    name,
    symbol,
    creator
    FROM tokens
    WHERE mint=?
    ORDER BY id DESC
    """,(r["mint"],))

    for x in cur.fetchall():
        print(
            x["id"],
            x["name"],
            x["symbol"],
            x["creator"]
        )

conn.close()