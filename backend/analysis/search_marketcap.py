import sqlite3


class SearchMarketCap:

    def __init__(self):
        self.conn = sqlite3.connect("backend/database/tokens.db")
        self.cursor = self.conn.cursor()

    def search(self, minimum_mc):

        self.cursor.execute("""
        SELECT
            name,
            symbol,
            mint,
            creator,
            market_cap_sol,
            sol_amount
        FROM tokens
        WHERE market_cap_sol >= ?
        ORDER BY market_cap_sol DESC
        LIMIT 20
        """, (minimum_mc,))

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    minimum = float(input("Minimum MarketCap : ").strip())

    finder = SearchMarketCap()

    rows = finder.search(minimum)

    print()
    print("========================================")
    print("SEARCH MARKET CAP")
    print("========================================")

    if not rows:

        print("Tidak ada token yang memenuhi kriteria.")

    else:

        for i, row in enumerate(rows, start=1):

            print(f"{i:>2}. {row[0]} ({row[1]})")
            print(f"    MarketCap : {row[4]:.2f}")
            print(f"    SOL       : {row[5]:.4f}")
            print(f"    Mint      : {row[2]}")
            print(f"    Creator   : {row[3]}")
            print()

    finder.close()