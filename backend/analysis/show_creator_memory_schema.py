import sqlite3

conn = sqlite3.connect("backend/database/tokens.db")

rows = conn.execute("""
PRAGMA table_info(creator_memory)
""").fetchall()

print("=" * 60)

for r in rows:
    print(r)

conn.close()