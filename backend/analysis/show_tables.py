import sqlite3

conn = sqlite3.connect("backend/database/solana.db")

rows = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""").fetchall()

print("=" * 60)

for r in rows:
    print(r[0])

conn.close()