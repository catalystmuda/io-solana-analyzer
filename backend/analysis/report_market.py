import sqlite3


class ReportMarket:

    def __init__(self):
        self.conn = sqlite3.connect("backend/database/tokens.db")
        self.cursor = self.conn.cursor()

    def generate(self):

        self.cursor.execute("""
        SELECT
            AVG(initial_buy),
            AVG(sol_amount),
            AVG(market_cap_sol),
            MAX(market_cap_sol),
            MIN(market_cap_sol)
        FROM tokens
        """)

        row = self.cursor.fetchone()

        return {
            "avg_initial_buy": row[0] or 0,
            "avg_sol": row[1] or 0,
            "avg_marketcap": row[2] or 0,
            "highest_marketcap": row[3] or 0,
            "lowest_marketcap": row[4] or 0
        }

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    report = ReportMarket()

    data = report.generate()

    print()
    print("========================================")
    print("MARKET DATASET")
    print("========================================")
    print(f"Average Initial Buy : {data['avg_initial_buy']:.4f}")
    print(f"Average SOL Amount  : {data['avg_sol']:.4f}")
    print(f"Average MarketCap   : {data['avg_marketcap']:.2f}")
    print(f"Highest MarketCap   : {data['highest_marketcap']:.2f}")
    print(f"Lowest MarketCap    : {data['lowest_marketcap']:.2f}")

    report.close()