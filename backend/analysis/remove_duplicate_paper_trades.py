import sqlite3

DB = "backend/database/tokens.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=" * 70)
print("REMOVE DUPLICATE PAPER TRADES")
print("=" * 70)

cur.execute("""
DELETE FROM paper_trades
WHERE id NOT IN (
    SELECT MIN(id)
    FROM paper_trades
    GROUP BY mint
)
""")

deleted = cur.rowcount

conn.commit()

total = cur.execute("""
SELECT COUNT(*)
FROM paper_trades
""").fetchone()[0]

conn.close()

print("DELETED :", deleted)
print("REMAIN  :", total)
print("=" * 70)