import sys
from backend.analysis.creator_intelligence_v21 import CreatorIntelligenceV21


class CreatorAlphaHunterV22:

    def __init__(self):
        self.engine = CreatorIntelligenceV21()


    def analyze_creator(self, creator):

        result = self.engine.analyze(creator)

        score = result.get(
            "final_score",
            0
        )

        alpha = result.get(
            "alpha_probability",
            0
        )

        rug = result.get(
            "rug_probability",
            100
        )

        decision = result.get(
            "decision",
            "UNKNOWN"
        )


        signals = result.get(
            "signals",
            []
        )


        hunter_score = score


        if alpha >= 80:
            hunter_score += 5


        if rug <= 20:
            hunter_score += 5


        if hunter_score > 100:
            hunter_score = 100


        if hunter_score >= 85:

            status = "ALPHA CANDIDATE"

        elif hunter_score >= 70:

            status = "WATCH"

        else:

            status = "IGNORE"


        return {

            "creator": creator,

            "hunter_score": hunter_score,

            "status": status,

            "alpha_probability": alpha,

            "rug_probability": rug,

            "decision": decision,

            "signals": signals

        }



if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Usage:"
        )

        print(
            "python -m backend.analysis.creator_alpha_hunter_v22 WALLET"
        )

        sys.exit()


    creator = sys.argv[1]


    hunter = CreatorAlphaHunterV22()


    result = hunter.analyze_creator(
        creator
    )


    print()
    print("==============================")
    print(" CREATOR ALPHA HUNTER V22 ")
    print("==============================")

    print(
        f"creator              : {result['creator']}"
    )

    print(
        f"hunter_score         : {result['hunter_score']}"
    )

    print(
        f"status               : {result['status']}"
    )

    print(
        f"alpha_probability    : {result['alpha_probability']}%"
    )

    print(
        f"rug_probability      : {result['rug_probability']}%"
    )

    print(
        f"decision             : {result['decision']}"
    )

    print(
        "signals              :",
        result["signals"]
    )
    