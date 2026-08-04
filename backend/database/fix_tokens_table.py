import sqlite3

DB = "backend/database/tokens.db"

conn = sqlite3.connect(DB)

print("=" * 70)
print("FIX TOKENS TABLE")
print("=" * 70)

conn.execute("""
ALTER TABLE tokens RENAME TO tokens_old;
""")

conn.execute("""
CREATE TABLE tokens (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    signature TEXT,

    mint TEXT UNIQUE,

    name TEXT,

    symbol TEXT,

    creator TEXT,

    tx_type TEXT,

    initial_buy REAL,

    sol_amount REAL,

    market_cap_sol REAL,

    bonding_curve TEXT,

    uri TEXT,

    pool TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    pair_address TEXT,

    dex TEXT,

    chain TEXT,

    liquidity REAL DEFAULT 0,

    volume24 REAL DEFAULT 0,

    fdv REAL DEFAULT 0,

    price_usd REAL DEFAULT 0,

    last_update TEXT

);
""")

conn.execute("""
INSERT OR IGNORE INTO tokens
SELECT *
FROM tokens_old;
""")

conn.execute("""
DROP TABLE tokens_old;
""")

conn.commit()

conn.close()

print("=" * 70)
print("DATABASE FIXED")
print("=" * 70)