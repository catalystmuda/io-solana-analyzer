import sqlite3
from datetime import datetime

DB = "backend/database/tokens.db"


def save_signal(mint, alpha):

    conn = sqlite3.connect(DB)

    conn.execute("""
    INSERT OR IGNORE INTO elite_signals
    (
        mint,
        detected_at,
        alpha,
        status
    )
    VALUES
    (
        ?,?,?,?
    )
    """,
    (
        mint,
        datetime.utcnow().isoformat(),
        alpha,
        "OPEN"
    ))

    conn.commit()
    conn.close()