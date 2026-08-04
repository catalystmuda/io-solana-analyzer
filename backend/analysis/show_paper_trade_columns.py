import sqlite3

conn = sqlite3.connect("backend/database/tokens.db")

rows = conn.execute("""
PRAGMA table_info(paper_trades)
""").fetchall()

print("=" * 70)
print("PAPER_TRADES COLUMNS")
print("=" * 70)

for row in rows:
    print(row)

conn.close()