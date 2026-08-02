import sqlite3


class CreatorAnalyzer:

    def __init__(self):
        self.conn = sqlite3.connect("backend/database/tokens.db")
        self.cursor = self.conn.cursor()

    def analyze(self, creator):

        self.cursor.execute("""
        SELECT
            COUNT(*),
            AVG(sol_amount),
            AVG(market_cap_sol),
            MAX(market_cap_sol),
            MIN(market_cap_sol),
            MIN(created_at),
            MAX(created_at)
        FROM tokens
        WHERE creator = ?
        """, (creator,))

        summary = self.cursor.fetchone()

        self.cursor.execute("""
        SELECT
            name,
            symbol,
            mint,
            market_cap_sol
        FROM tokens
        WHERE creator = ?
        ORDER BY market_cap_sol DESC
        LIMIT 1
        """, (creator,))

        best = self.cursor.fetchone()

        self.cursor.execute("""
        SELECT
            name,
            symbol,
            mint,
            market_cap_sol
        FROM tokens
        WHERE creator = ?
        ORDER BY market_cap_sol ASC
        LIMIT 1
        """, (creator,))

        worst = self.cursor.fetchone()

        return summary, best, worst

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    creator = input("Creator Address : ").strip()

    analyzer = CreatorAnalyzer()

    summary, best, worst = analyzer.analyze(creator)

    if summary[0] == 0:
        print("\nCreator tidak ditemukan.")
        analyzer.close()
        exit()

    print("\n========================================")
    print("CREATOR ANALYZER")
    print("========================================")

    print(f"Total Token       : {summary[0]}")
    print(f"Average SOL       : {summary[1]:.4f}")
    print(f"Average MarketCap : {summary[2]:.2f}")
    print(f"Highest MarketCap : {summary[3]:.2f}")
    print(f"Lowest MarketCap  : {summary[4]:.2f}")
    print(f"First Token       : {summary[5]}")
    print(f"Latest Token      : {summary[6]}")

    print("\nBEST TOKEN")
    print("----------------------------------------")
    print(f"Name       : {best[0]} ({best[1]})")
    print(f"Mint       : {best[2]}")
    print(f"MarketCap  : {best[3]:.2f}")

    print("\nWORST TOKEN")
    print("----------------------------------------")
    print(f"Name       : {worst[0]} ({worst[1]})")
    print(f"Mint       : {worst[2]}")
    print(f"MarketCap  : {worst[3]:.2f}")

    print("\nAI SUMMARY")
    print("----------------------------------------")

    if summary[0] >= 50:
        print("✔ Creator sangat aktif.")
    elif summary[0] >= 20:
        print("✔ Creator cukup aktif.")
    else:
        print("✔ Creator masih memiliki riwayat sedikit.")

    if summary[3] >= 100:
        print("✔ Pernah membuat token dengan market cap tinggi.")
    else:
        print("• Belum ada token dengan market cap tinggi.")

    if summary[2] >= 50:
        print("✔ Rata-rata kualitas token cukup baik.")
    else:
        print("• Rata-rata market cap masih rendah.")

    analyzer.close()