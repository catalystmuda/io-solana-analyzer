import sqlite3


DB = "backend/database/tokens.db"


def create_table():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS smart_wallet_memory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        wallet TEXT UNIQUE,

        total_trades INTEGER DEFAULT 0,

        alpha_hits INTEGER DEFAULT 0,

        win_rate REAL DEFAULT 0,

        average_roi REAL DEFAULT 0,

        best_token TEXT,

        best_roi REAL DEFAULT 0,

        risk_score INTEGER DEFAULT 0,

        reputation TEXT DEFAULT 'UNKNOWN',

        signals TEXT,

        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    conn.commit()
    conn.close()


    print("==============================")
    print(" SMART WALLET MEMORY CREATED ")
    print("==============================")


if __name__ == "__main__":
    create_table()