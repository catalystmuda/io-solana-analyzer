import sqlite3

DB = "backend/database/tokens.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
UPDATE paper_trades
SET status='WIN'
WHERE roi_percent>=100
""")

win = cur.rowcount

cur.execute("""
UPDATE paper_trades
SET status='LOSS'
WHERE roi_percent<=-50
""")

loss = cur.rowcount

conn.commit()
conn.close()

print("=" * 70)
print("PAPER TRADE CLOSED")
print("=" * 70)
print("WIN  :", win)
print("LOSS :", loss)
print("=" * 70)