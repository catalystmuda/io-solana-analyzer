import sqlite3
import os

db = "backend/database/solana.db"

print("=" * 60)
print("DB EXISTS :", os.path.exists(db))
print("DB PATH   :", os.path.abspath(db))

conn = sqlite3.connect(db)

rows = conn.execute("""
SELECT name
FROM sqlite_master
""").fetchall()

print("=" * 60)

for r in rows:
    print(r)

conn.close()