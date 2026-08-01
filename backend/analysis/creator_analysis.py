import sqlite3


class CreatorAnalysis:

    def __init__(self):
        self.conn = sqlite3.connect(
    "backend/database/tokens.db"
)
        self.cursor = self.conn.cursor()

    def top_creators(self, limit=10):

        self.cursor.execute("""
        SELECT
            creator,
            COUNT(*) AS total_tokens,
            AVG(initial_buy) AS avg_initial_buy,
            AVG(market_cap_sol) AS avg_market_cap,
            MAX(market_cap_sol) AS highest_market_cap,
            MIN(market_cap_sol) AS lowest_market_cap,
            MIN(received_at) AS first_seen,
            MAX(received_at) AS last_seen
        FROM tokens
        GROUP BY creator
        ORDER BY total_tokens DESC
        LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    analysis = CreatorAnalysis()

    print("\n========================================")
    print("CREATOR PROFILE")
    print("========================================\n")

    creators = analysis.top_creators()

    for i, creator in enumerate(creators, start=1):

        print(f"Creator #{i}")
        print(f"Address            : {creator[0]}")
        print(f"Total Token        : {creator[1]}")
        print(f"Average InitialBuy : {creator[2]:.4f} SOL")
        print(f"Average MarketCap  : {creator[3]:.2f} SOL")
        print(f"Highest MarketCap  : {creator[4]:.2f} SOL")
        print(f"Lowest MarketCap   : {creator[5]:.2f} SOL")
        print(f"First Seen         : {creator[6]}")
        print(f"Last Seen          : {creator[7]}")
        print("-" * 60)

    analysis.close()