import sqlite3


class PatternAnalyzer:

    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()

    # =====================================
    # Dataset Statistics
    # =====================================

    def dataset_statistics(self):

        print()
        print("=" * 40)
        print("PATTERN ANALYZER")
        print("=" * 40)

        # Total Token
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM tokens
        """)

        total_tokens = self.cursor.fetchone()[0]

        # Total Creator
        self.cursor.execute("""
            SELECT COUNT(DISTINCT creator)
            FROM tokens
        """)

        total_creators = self.cursor.fetchone()[0]

        # Average Token per Creator
        if total_creators > 0:
            avg_token_creator = total_tokens / total_creators
        else:
            avg_token_creator = 0

        print()
        print("DATASET")
        print("-" * 40)

        print(f"Total Tokens              : {total_tokens}")
        print(f"Unique Creators           : {total_creators}")
        print(f"Average Token / Creator   : {avg_token_creator:.2f}")

    # =====================================
    # Close
    # =====================================

    def close(self):

        self.conn.close()


if __name__ == "__main__":

    analyzer = PatternAnalyzer()

    analyzer.dataset_statistics()

    analyzer.close()