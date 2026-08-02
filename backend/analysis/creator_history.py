import sqlite3


class CreatorHistory:

    def __init__(self):
        self.conn = sqlite3.connect("backend/database/tokens.db")
        self.cursor = self.conn.cursor()

    def history(self, creator):

        self.cursor.execute("""
        SELECT
            created_at,
            name,
            symbol,
            mint,
            sol_amount,
            market_cap_sol
        FROM tokens
        WHERE creator = ?
        ORDER BY datetime(created_at) DESC
        """, (creator,))

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    creator = input("Creator Address : ").strip()

    history = CreatorHistory()

    rows = history.history(creator)

    print()
    print("========================================")
    print("CREATOR HISTORY")
    print("========================================")

    if not rows:

        print("Creator tidak ditemukan.")

    else:

        print(f"Total Token : {len(rows)}")
        print("----------------------------------------")

        for i, row in enumerate(rows, start=1):

            print(f"{i:>2}. {row[1]} ({row[2]})")
            print(f"    Date      : {row[0]}")
            print(f"    Mint      : {row[3]}")
            print(f"    SOL       : {row[4]:.4f}")
            print(f"    MarketCap : {row[5]:.2f}")
            print()

    history.close()