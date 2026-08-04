import sqlite3

DB = "backend/database/tokens.db"

conn = sqlite3.connect(DB)

columns = [

    ("current_fdv", "REAL DEFAULT 0"),
    ("ath_fdv", "REAL DEFAULT 0"),
    ("current_price", "REAL DEFAULT 0"),
    ("roi", "REAL DEFAULT 0"),
    ("last_checked", "TEXT")

]

existing = []

for row in conn.execute("PRAGMA table_info(elite_signals);"):
    existing.append(row[1])

for name, definition in columns:

    if name not in existing:

        conn.execute(f"""
        ALTER TABLE elite_signals
        ADD COLUMN {name} {definition}
        """)

        print("ADD :", name)

conn.commit()
conn.close()

print("=" * 70)
print("PAPER TRADE DATABASE READY")
print("=" * 70)