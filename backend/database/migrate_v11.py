import sqlite3

conn = sqlite3.connect("backend/database/tokens.db")

columns = [
    "ALTER TABLE tokens ADD COLUMN pair_address TEXT",
    "ALTER TABLE tokens ADD COLUMN dex TEXT",
    "ALTER TABLE tokens ADD COLUMN chain TEXT",
    "ALTER TABLE tokens ADD COLUMN liquidity REAL DEFAULT 0",
    "ALTER TABLE tokens ADD COLUMN volume24 REAL DEFAULT 0",
    "ALTER TABLE tokens ADD COLUMN fdv REAL DEFAULT 0",
    "ALTER TABLE tokens ADD COLUMN price_usd REAL DEFAULT 0",
    "ALTER TABLE tokens ADD COLUMN last_update TEXT"
]

for sql in columns:
    try:
        conn.execute(sql)
    except Exception:
        pass

conn.commit()
conn.close()

print("=" * 60)
print("DATABASE MIGRATION V1.1 FINISHED")
print("=" * 60)