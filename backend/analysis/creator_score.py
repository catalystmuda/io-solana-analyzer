import sqlite3

from backend.engine.scoring import ScoringEngine


class CreatorScore:

    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()

    # =====================================
    # Hitung Score Creator
    # =====================================

    def calculate(self, creator):

        self.cursor.execute(
            """
            SELECT
                COUNT(*),
                AVG(sol_amount),
                AVG(market_cap_sol),
                MAX(market_cap_sol),
                MIN(market_cap_sol)
            FROM tokens
            WHERE creator = ?
            """,
            (creator,)
        )

        row = self.cursor.fetchone()

        if row is None:
            return None

        total_token = row[0] or 0
        avg_sol = row[1] or 0
        avg_mc = row[2] or 0
        highest_mc = row[3] or 0
        lowest_mc = row[4] or 0

        if total_token == 0:
            return None

        creator_score = ScoringEngine.creator_score(
            total_token,
            avg_sol,
            avg_mc,
            highest_mc,
            lowest_mc
        )

        risk_score = ScoringEngine.risk_score(
            total_token,
            avg_sol,
            avg_mc
        )

        pattern_score = ScoringEngine.pattern_score(
            total_token,
            highest_mc,
            lowest_mc
        )

        ai_score = ScoringEngine.ai_score(
            creator_score,
            risk_score,
            pattern_score
        )

        return {
            "creator": creator,
            "total_token": total_token,
            "avg_sol": avg_sol,
            "avg_marketcap": avg_mc,
            "highest_marketcap": highest_mc,
            "lowest_marketcap": lowest_mc,
            "creator_score": creator_score,
            "risk_score": risk_score,
            "pattern_score": pattern_score,
            "ai_score": ai_score,
            "rating": ScoringEngine.rating(ai_score),
            "confidence": ScoringEngine.confidence(total_token),
            "reputation": ScoringEngine.reputation(creator_score)
        }

    def close(self):

        self.conn.close()


if __name__ == "__main__":

    creator = input("Creator Address : ").strip()

    analyzer = CreatorScore()

    result = analyzer.calculate(creator)

    print()
    print("========================================")
    print("CREATOR SCORE")
    print("========================================")

    if result is None:

        print("Creator tidak ditemukan.")

    else:

        print(f"Creator            : {result['creator']}")
        print(f"Total Token        : {result['total_token']}")
        print(f"Average SOL        : {result['avg_sol']:.4f}")
        print(f"Average MarketCap  : {result['avg_marketcap']:.2f}")
        print(f"Highest MarketCap  : {result['highest_marketcap']:.2f}")
        print(f"Lowest MarketCap   : {result['lowest_marketcap']:.2f}")

        print("----------------------------------------")

        print(f"Creator Score      : {result['creator_score']}/100")
        print(f"Risk Score         : {result['risk_score']}/100")
        print(f"Pattern Score      : {result['pattern_score']}/100")
        print(f"AI Score           : {result['ai_score']}/100")

        print("----------------------------------------")

        print(f"Rating             : {result['rating']}")
        print(f"Confidence         : {result['confidence']}")
        print(f"Reputation         : {result['reputation']}")

    analyzer.close()