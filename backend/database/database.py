import sqlite3
from datetime import datetime


class Database:

    def __init__(self):

        print("[Database] Ready")

        self.conn = sqlite3.connect("tokens.db")
        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            received_at TEXT,

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

            pool TEXT

        )
        """)

        self.conn.commit()

    def save_token(self, token):

        received_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:

            self.cursor.execute("""
            INSERT OR IGNORE INTO tokens (

                received_at,
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

            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (

                received_at,
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

            print(f"[Database] Saved : {token['symbol']}")

        except Exception as e:

            print(f"[Database Error] {e}")

    def close(self):

        self.conn.close()