import sqlite3


class TokenReport:

    def __init__(self):
        self.conn = sqlite3.connect("backend/database/tokens.db")
        self.cursor = self.conn.cursor()

    def get_token(self, mint):

        self.cursor.execute("""
        SELECT
            signature,
            mint,
            name,
            symbol,
            creator,
            tx_type,
            initial_buy,
            sol_amount,
            market_cap_sol,
            bonding_curve,
            uri,
            pool,
            created_at
        FROM tokens
        WHERE mint = ?
        """, (mint,))

        row = self.cursor.fetchone()

        if row is None:
            return None

        return {
            "signature": row[0],
            "mint": row[1],
            "name": row[2],
            "symbol": row[3],
            "creator": row[4],
            "tx_type": row[5],
            "initial_buy": row[6],
            "sol_amount": row[7],
            "market_cap_sol": row[8],
            "bonding_curve": row[9],
            "uri": row[10],
            "pool": row[11],
            "created_at": row[12]
        }

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    mint = input("Mint Address : ").strip()

    report = TokenReport()

    token = report.get_token(mint)

    print()
    print("========================================")
    print("TOKEN REPORT")
    print("========================================")

    if token is None:

        print("Token tidak ditemukan.")

    else:

        print(f"Name            : {token['name']}")
        print(f"Symbol          : {token['symbol']}")
        print(f"Mint            : {token['mint']}")
        print(f"Creator         : {token['creator']}")
        print(f"Transaction     : {token['tx_type']}")
        print(f"Initial Buy     : {token['initial_buy']}")
        print(f"SOL Amount      : {token['sol_amount']}")
        print(f"MarketCap       : {token['market_cap_sol']}")
        print(f"Bonding Curve   : {token['bonding_curve']}")
        print(f"URI             : {token['uri']}")
        print(f"Pool            : {token['pool']}")
        print(f"Signature       : {token['signature']}")
        print(f"Created At      : {token['created_at']}")

    report.close()