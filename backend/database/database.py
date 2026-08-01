import sqlite3


class Database:

    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db",
            check_same_thread=False
        )

        self.create_table()

        print("[Database] Ready")

    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            signature TEXT,
            mint TEXT,
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

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.conn.commit()

    def save_token(self, token):

        cursor = self.conn.cursor()

        # -----------------------------
        # Jangan simpan jika mint sudah ada
        # -----------------------------

        cursor.execute(
            "SELECT id FROM tokens WHERE mint = ?",
            (token["mint"],)
        )

        exists = cursor.fetchone()

        if exists:

            print(f"[Database] Skip Duplicate : {token['symbol']}")

            return

        # -----------------------------
        # Simpan Token Baru
        # -----------------------------

        cursor.execute("""
        INSERT INTO tokens (

            signature,
            mint,
            name,
            symbol,
            creator,
            tx_type,
            initial_buy,
            sol_amount,
            market_cap_sol,
            bonding_curve,
            uri,
            pool

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            token["signature"],
            token["mint"],
            token["name"],
            token["symbol"],
            token["creator"],
            token["tx_type"],
            token["initial_buy"],
            token["sol_amount"],
            token["market_cap_sol"],
            token["bonding_curve"],
            token["uri"],
            token["pool"]

        ))

        self.conn.commit()

        cursor.execute("SELECT COUNT(*) FROM tokens")

        total = cursor.fetchone()[0]

        print(f"[Database] Saved : {token['symbol']} | Total Dataset : {total}")

    def close(self):

        self.conn.close()