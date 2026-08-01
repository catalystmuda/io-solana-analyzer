import sqlite3


class CreatorProfile:

    def __init__(self):

        self.conn = sqlite3.connect(
    "backend/database/tokens.db"
)
        self.cursor = self.conn.cursor()

    def get_profile(self, creator):

        self.cursor.execute("""
            SELECT
                creator,
                COUNT(*),
                AVG(sol_amount),
                AVG(initial_buy),
                AVG(market_cap_sol),
                MAX(market_cap_sol),
                MIN(market_cap_sol),
                MIN(received_at),
                MAX(received_at)
            FROM tokens
            WHERE creator=?
        """, (creator,))

        return self.cursor.fetchone()

    def get_tokens(self, creator):

        self.cursor.execute("""
            SELECT
                symbol,
                market_cap_sol,
                sol_amount,
                received_at
            FROM tokens
            WHERE creator=?
            ORDER BY received_at DESC
        """, (creator,))

        return self.cursor.fetchall()

    def close(self):

        self.conn.close()


if __name__ == "__main__":

    creator_address = input("Creator Address : ").strip()

    profile = CreatorProfile()

    info = profile.get_profile(creator_address)

    if info is None or info[0] is None:

        print("\nCreator tidak ditemukan.")

    else:

        print("\n========================================")
        print("CREATOR PROFILE")
        print("========================================")

        print(f"\nCreator            : {info[0]}")
        print(f"Total Token        : {info[1]}")
        print(f"Average SOL        : {info[2]:.6f}")
        print(f"Average Buy Token  : {info[3]:,.0f}")
        print(f"Average MarketCap  : {info[4]:.2f} SOL")
        print(f"Highest MarketCap  : {info[5]:.2f} SOL")
        print(f"Lowest MarketCap   : {info[6]:.2f} SOL")
        print(f"First Seen         : {info[7]}")
        print(f"Last Seen          : {info[8]}")

        print("\n========================================")
        print("TOKENS")
        print("========================================")

        tokens = profile.get_tokens(creator_address)

        for i, token in enumerate(tokens, start=1):

            print(
                f"{i}. {token[0]} | "
                f"MC {token[1]:.2f} SOL | "
                f"SOL {token[2]:.4f} | "
                f"{token[3]}"
            )

    profile.close()