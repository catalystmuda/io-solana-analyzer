import sqlite3


class SearchMint:

    def __init__(self):
        self.conn = sqlite3.connect("backend/database/tokens.db")
        self.cursor = self.conn.cursor()

    def search(self, keyword):

        self.cursor.execute("""
        SELECT
            mint,
            name,
            symbol,
            creator,
            market_cap_sol,
            sol_amount
        FROM tokens
        WHERE mint LIKE ?
        ORDER BY created_at DESC
        LIMIT 20
        """, (f"%{keyword}%",))

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    keyword = input("Search Mint : ").strip()

    finder = SearchMint()

    rows = finder.search(keyword)

    print()
    print("========================================")
    print("SEARCH MINT")
    print("========================================")

    if not rows:

        print("Mint tidak ditemukan.")

    else:

        for i, row in enumerate(rows, start=1):

            print(f"{i:>2}. {row[0]}")
            print(f"    Name      : {row[1]}")
            print(f"    Symbol    : {row[2]}")
            print(f"    Creator   : {row[3]}")
            print(f"    MarketCap : {row[4]:.2f}")
            print(f"    SOL       : {row[5]:.4f}")
            print()

    finder.close()