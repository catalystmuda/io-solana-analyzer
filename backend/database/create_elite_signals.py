import sqlite3

DB = "backend/database/tokens.db"

conn = sqlite3.connect(DB)

conn.execute("""
CREATE TABLE IF NOT EXISTS elite_signals (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    mint TEXT UNIQUE,

    name TEXT,

    symbol TEXT,

    creator TEXT,

    alpha_score REAL,

    market_cap_sol REAL,

    liquidity REAL,

    volume24 REAL,

    fdv REAL,

    category TEXT,

    reputation_score REAL,

    breakout_count INTEGER,

    survivor_count INTEGER,

    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    status TEXT DEFAULT 'OPEN'

)
""")

conn.commit()
conn.close()

print("=" * 70)
print("ELITE SIGNAL TABLE READY")
print("=" * 70)