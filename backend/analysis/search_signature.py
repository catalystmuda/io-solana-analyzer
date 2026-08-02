import sqlite3


class SearchSignature:

    def __init__(self):
        self.conn = sqlite3.connect("backend/database/tokens.db")
        self.cursor = self.conn.cursor()

    def search(self, keyword):

        self.cursor.execute("""
        SELECT
            signature,
            name,
            symbol,
            mint,
            creator,
            market_cap_sol
        FROM tokens
        WHERE signature LIKE ?
        ORDER BY created_at DESC
        LIMIT 20
        """, (f"%{keyword}%",))

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    keyword = input("Search Signature : ").strip()

    finder = SearchSignature()

    rows = finder.search(keyword)

    print()
    print("========================================")
    print("SEARCH SIGNATURE")
    print("========================================")

    if not rows:

        print("Signature tidak ditemukan.")

    else:

        for i, row in enumerate(rows, start=1):

            print(f"{i:>2}. {row[0]}")
            print(f"    Name      : {row[1]} ({row[2]})")
            print(f"    Mint      : {row[3]}")
            print(f"    Creator   : {row[4]}")
            print(f"    MarketCap : {row[5]:.2f}")
            print()

    finder.close()