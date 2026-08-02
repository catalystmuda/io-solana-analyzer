from backend.analysis.creator_score import CreatorScore
from backend.analysis.creator_history import CreatorHistory


class CreatorAnalyzerV2:

    def __init__(self):

        self.score = CreatorScore()
        self.history = CreatorHistory()

    def analyze(self, creator):

        score = self.score.calculate(creator)
        history = self.history.history(creator)

        return score, history

    def close(self):

        self.score.close()
        self.history.close()


if __name__ == "__main__":

    creator = input("Creator Address : ").strip()

    analyzer = CreatorAnalyzerV2()

    score, history = analyzer.analyze(creator)

    if score is None:

        print("\nCreator tidak ditemukan.")
        analyzer.close()
        exit()

    print("\n========================================")
    print("      CREATOR ANALYZER V2")
    print("========================================")

    print(f"Creator            : {score['creator']}")
    print(f"Total Token        : {score['total_token']}")
    print(f"Average SOL        : {score['avg_sol']:.4f}")
    print(f"Average MarketCap  : {score['avg_marketcap']:.2f}")

    print("----------------------------------------")

    print(f"Creator Score      : {score['creator_score']}/100")
    print(f"Risk Score         : {score['risk_score']}/100")
    print(f"Pattern Score      : {score['pattern_score']}/100")
    print(f"AI Score           : {score['ai_score']}/100")

    print("----------------------------------------")

    print(f"Rating             : {score['rating']}")
    print(f"Confidence         : {score['confidence']}")
    print(f"Reputation         : {score['reputation']}")

    print("----------------------------------------")
    print(f"History Token      : {len(history)}")

    print("\nLAST 10 TOKENS")
    print("----------------------------------------")

    for row in history[:10]:
        print(f"{row[0]} | {row[1]} ({row[2]}) | MC {row[5]:.2f}")

    analyzer.close()