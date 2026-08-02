import sqlite3


class ReportGeneral:

    def __init__(self):
        self.conn = sqlite3.connect("backend/database/tokens.db")
        self.cursor = self.conn.cursor()

    def generate(self):

        self.cursor.execute("SELECT COUNT(*) FROM tokens")
        total_token = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(DISTINCT mint) FROM tokens")
        total_mint = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(DISTINCT creator) FROM tokens")
        total_creator = self.cursor.fetchone()[0]

        duplicate = total_token - total_mint

        avg_token_creator = 0

        if total_creator > 0:
            avg_token_creator = total_token / total_creator

        return {
            "total_token": total_token,
            "total_mint": total_mint,
            "total_creator": total_creator,
            "duplicate": duplicate,
            "avg_token_creator": avg_token_creator
        }

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    report = ReportGeneral()

    data = report.generate()

    print()
    print("========================================")
    print("GENERAL DATASET")
    print("========================================")
    print(f"Total Token          : {data['total_token']}")
    print(f"Unique Mint          : {data['total_mint']}")
    print(f"Unique Creator       : {data['total_creator']}")
    print(f"Duplicate Token      : {data['duplicate']}")
    print(f"Average TokenCreator : {data['avg_token_creator']:.2f}")

    report.close()