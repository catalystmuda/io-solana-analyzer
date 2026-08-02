import sqlite3


DB = "backend/database/tokens.db"


def create_table():

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallet_activity (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        wallet TEXT,

        token_mint TEXT,

        token_symbol TEXT,

        token_name TEXT,

        creator TEXT,

        signature TEXT,

        entry_mc REAL DEFAULT 0,

        exit_mc REAL DEFAULT 0,

        roi REAL DEFAULT 0,

        result TEXT DEFAULT 'UNKNOWN',

        buy_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    conn.commit()

    conn.close()


    print("==============================")
    print(" WALLET ACTIVITY TABLE CREATED ")
    print("==============================")


if __name__ == "__main__":
    create_table()