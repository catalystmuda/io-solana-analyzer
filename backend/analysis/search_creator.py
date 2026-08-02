import sqlite3


class SearchCreator:

    def __init__(self):
        self.conn = sqlite3.connect("backend/database/tokens.db")
        self.cursor = self.conn.cursor()

    def search(self, keyword):

        self.cursor.execute("""
        SELECT
            creator,
            COUNT(*) AS total,
            AVG(market_cap_sol) AS avg_mc,
            AVG(sol_amount) AS avg_sol
        FROM tokens
        WHERE creator LIKE ?
        GROUP BY creator
        ORDER BY total DESC
        """, (f"%{keyword}%",))

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    keyword = input("Search Creator : ").strip()

    finder = SearchCreator()

    rows = finder.search(keyword)

    print()
    print("========================================")
    print("SEARCH CREATOR")
    print("========================================")

    if not rows:

        print("Creator tidak ditemukan.")

    else:

        for i, row in enumerate(rows, start=1):

            print(f"{i:>2}. {row[0]}")
            print(f"    Total Token : {row[1]}")
            print(f"    Avg SOL     : {row[3]:.4f}")
            print(f"    Avg MC      : {row[2]:.2f}")
            print()

    finder.close()