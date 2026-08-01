import sqlite3


class HistoryDatabase:

    def __init__(self):

        self.conn = sqlite3.connect("tokens.db")
        self.cursor = self.conn.cursor()

    def total_tokens(self):

        self.cursor.execute("SELECT COUNT(*) FROM tokens")
        return self.cursor.fetchone()[0]

    def total_creators(self):

        self.cursor.execute("""
            SELECT COUNT(DISTINCT creator)
            FROM tokens
        """)
        return self.cursor.fetchone()[0]

    def total_mints(self):

        self.cursor.execute("""
            SELECT COUNT(DISTINCT mint)
            FROM tokens
        """)
        return self.cursor.fetchone()[0]

    def duplicate_tokens(self):

        self.cursor.execute("""
            SELECT COUNT(*) - COUNT(DISTINCT mint)
            FROM tokens
        """)
        return self.cursor.fetchone()[0]

    def latest_tokens(self, limit=10):

        self.cursor.execute("""
            SELECT
                received_at,
                symbol,
                creator,
                market_cap_sol
            FROM tokens
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()

    def close(self):

        self.conn.close()