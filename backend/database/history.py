import sqlite3


class HistoryDatabase:

    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

    # ==========================================
    # Total Token
    # ==========================================

    def total_tokens(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM tokens
        """)

        return self.cursor.fetchone()[0]

    # ==========================================
    # Total Creator
    # ==========================================

    def total_creators(self):

        self.cursor.execute("""
            SELECT COUNT(DISTINCT creator)
            FROM tokens
        """)

        return self.cursor.fetchone()[0]

    # ==========================================
    # Total Mint
    # ==========================================

    def total_mints(self):

        self.cursor.execute("""
            SELECT COUNT(DISTINCT mint)
            FROM tokens
        """)

        return self.cursor.fetchone()[0]

    # ==========================================
    # Duplicate Records
    # ==========================================

    def duplicate_tokens(self):

        self.cursor.execute("""
            SELECT COUNT(*) - COUNT(DISTINCT mint)
            FROM tokens
        """)

        return self.cursor.fetchone()[0]

    # ==========================================
    # Latest Tokens
    # ==========================================

    def latest_tokens(self, limit=10):

        self.cursor.execute("""
            SELECT
                created_at,
                symbol,
                creator,
                market_cap_sol
            FROM tokens
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()

    # ==========================================
    # Close
    # ==========================================

    def close(self):

        self.conn.close()