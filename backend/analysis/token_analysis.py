import sqlite3


class TokenAnalysis:

    def __init__(self):
        self.conn = sqlite3.connect(
    "backend/database/tokens.db"
)
        self.cursor = self.conn.cursor()

    def latest_tokens(self, limit=10):

        self.cursor.execute("""
            SELECT
                name,
                symbol,
                mint,
                creator,
                initial_buy,
                sol_amount,
                market_cap_sol,
                pool,
                uri,
                received_at
            FROM tokens
            ORDER BY received_at DESC
            LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    analysis = TokenAnalysis()

    print("\n========================================")
    print("TOKEN PROFILE")
    print("========================================\n")

    tokens = analysis.latest_tokens()

    for i, token in enumerate(tokens, start=1):

        print(f"Token #{i}")
        print(f"Name              : {token[0]}")
        print(f"Symbol            : {token[1]}")
        print(f"Mint              : {token[2]}")
        print(f"Creator           : {token[3]}")
        print(f"Initial Buy       : {token[4]:,.0f} Tokens")
        print(f"SOL Invested      : {token[5]:.6f} SOL")
        print(f"MarketCap         : {token[6]:.2f} SOL")
        print(f"Pool              : {token[7]}")
        print(f"Metadata URI      : {token[8]}")
        print(f"Created At        : {token[9]}")
        print("-" * 70)

    analysis.close()