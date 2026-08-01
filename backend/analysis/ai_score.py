import sqlite3

from backend.engine.scoring import ScoringEngine


class AIScore:

    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()

    # ==========================================
    # Creator Statistics
    # ==========================================

    def get_creator_stats(self, creator):

        self.cursor.execute("""

            SELECT

                COUNT(*),
                AVG(sol_amount),
                AVG(market_cap_sol),
                MAX(market_cap_sol),
                MIN(market_cap_sol)

            FROM tokens

            WHERE creator = ?

        """, (creator,))

        row = self.cursor.fetchone()

        if row is None:
            return None

        total = row[0] or 0

        if total == 0:
            return None

        return {

            "total": total,
            "avg_sol": row[1] or 0,
            "avg_mc": row[2] or 0,
            "highest": row[3] or 0,
            "lowest": row[4] or 0

        }

    # ==========================================
    # AI Analyze
    # ==========================================

    def analyze(self, creator):

        stats = self.get_creator_stats(creator)

        if stats is None:
            return None

        creator_score = ScoringEngine.creator_score(
            stats["total"],
            stats["avg_sol"],
            stats["avg_mc"],
            stats["highest"],
            stats["lowest"]
        )

        risk_score = ScoringEngine.risk_score(
            stats["total"],
            stats["avg_sol"],
            stats["avg_mc"]
        )

        pattern_score = ScoringEngine.pattern_score(
            stats["total"],
            stats["highest"],
            stats["lowest"]
        )

        ai_score = ScoringEngine.ai_score(
            creator_score,
            risk_score,
            pattern_score
        )

        rating = ScoringEngine.rating(ai_score)

        confidence = ScoringEngine.confidence(
            stats["total"]
        )

        reputation = ScoringEngine.reputation(
            creator_score
        )

        return {

            "creator": creator,

            "total_token": stats["total"],

            "avg_sol": stats["avg_sol"],

            "avg_marketcap": stats["avg_mc"],

            "highest_marketcap": stats["highest"],

            "lowest_marketcap": stats["lowest"],

            "creator_score": creator_score,

            "risk_score": risk_score,

            "pattern_score": pattern_score,

            "ai_score": ai_score,

            "rating": rating,

            "confidence": confidence,

            "reputation": reputation

        }

    # ==========================================

    def close(self):

        self.conn.close()


if __name__ == "__main__":

    creator = input("Creator Address : ").strip()

    analyzer = AIScore()

    result = analyzer.analyze(creator)

    print()

    print("========================================")
    print("AI SCORE")
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