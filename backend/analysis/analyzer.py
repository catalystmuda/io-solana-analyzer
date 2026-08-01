from backend.analysis.creator_score import CreatorScore


def main():

    print()
    print("========================================")
    print("      SOLANA AI ANALYZER v1.0")
    print("========================================")
    print()

    creator = input("Creator Address : ").strip()

    analyzer = CreatorScore()

    result = analyzer.calculate(creator)

    print()

    if result is None:

        print("Creator tidak ditemukan.")

        analyzer.close()

        return

    print("========================================")
    print("ANALYSIS RESULT")
    print("========================================")

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
    print(f"Reputation         : {result['reputation']}")
    print(f"Confidence         : {result['confidence']}")

    print("----------------------------------------")

    if result["rating"] == "A+":

        print("Recommendation : Strong Buy")

    elif result["rating"] == "A":

        print("Recommendation : Buy")

    elif result["rating"] == "B":

        print("Recommendation : Watchlist")

    elif result["rating"] == "C":

        print("Recommendation : Observe")

    else:

        print("Recommendation : High Risk")

    print()
    print("========================================")

    analyzer.close()


if __name__ == "__main__":
    main()