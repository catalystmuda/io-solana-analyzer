import sqlite3


class ReportCreator:

    def __init__(self):
        self.conn = sqlite3.connect("backend/database/tokens.db")
        self.cursor = self.conn.cursor()

    def generate(self):

        self.cursor.execute("""
        SELECT
            creator,
            COUNT(*) AS total
        FROM tokens
        GROUP BY creator
        ORDER BY total DESC
        LIMIT 10
        """)

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    report = ReportCreator()

    creators = report.generate()

    print()
    print("========================================")
    print("TOP 10 CREATOR")
    print("========================================")

    no = 1

    for creator, total in creators:

        print(f"{no:>2}. {creator} ({total} token)")
        no += 1

    report.close()