import sqlite3


DB = "backend/database/tokens.db"


def create_table():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS creator_memory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        creator TEXT UNIQUE,

        total_tokens INTEGER DEFAULT 0,

        highest_mc REAL DEFAULT 0,

        average_mc REAL DEFAULT 0,

        breakout_count INTEGER DEFAULT 0,

        survivor_count INTEGER DEFAULT 0,

        reputation_score INTEGER DEFAULT 0,

        risk_score INTEGER DEFAULT 0,

        category TEXT,

        signals TEXT,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    conn.commit()

    conn.close()


    print("creator_memory table created")



if __name__ == "__main__":

    create_table()