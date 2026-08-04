import sqlite3

DB = "backend/database/tokens.db"

conn = sqlite3.connect(DB)

try:

    conn.execute("""
    ALTER TABLE tokens
    ADD COLUMN alpha_score REAL DEFAULT 0
    """)

    print("=" * 70)
    print("alpha_score column added")
    print("=" * 70)

except Exception as e:

    print("=" * 70)
    print(e)
    print("=" * 70)

conn.commit()
conn.close()