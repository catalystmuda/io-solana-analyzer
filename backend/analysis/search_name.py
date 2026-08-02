import sqlite3


class SearchName:

    def __init__(self):
        self.conn = sqlite3.connect("backend/database/tokens.db")
        self.cursor = self.conn.cursor()

    def search(self, keyword):

        self.cursor.execute("""
        SELECT
            name,
            symbol,
            mint,
            creator,
            market_cap_sol,
            sol_amount
        FROM tokens
        WHERE name LIKE ?
        ORDER BY market_cap_sol DESC
        LIMIT 20
        """, (f"%{keyword}%",))

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    keyword = input("Search Name : ").strip()

    finder = SearchName()

    rows = finder.search(keyword)

    print()
    print("========================================")
    print("SEARCH NAME")
    print("========================================")

    if not rows:

        print("Nama token tidak ditemukan.")

    else:

        for i, row in enumerate(rows, start=1):

            print(f"{i:>2}. {row[0]} ({row[1]})")
            print(f"    Mint      : {row[2]}")
            print(f"    Creator   : {row[3]}")
            print(f"    MarketCap : {row[4]:.2f}")
            print(f"    SOL       : {row[5]:.4f}")
            print()

    finder.close()