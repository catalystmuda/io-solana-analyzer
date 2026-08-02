from backend.analysis.creator_alpha_score import CreatorAlphaScore
from backend.analysis.creator_risk_normalizer import CreatorRiskNormalizer
from backend.analysis.creator_pattern_memory import CreatorPatternMemory
from backend.analysis.creator_network import CreatorNetwork


class CreatorIntelligenceV17:

    def __init__(self):
        self.alpha = CreatorAlphaScore()
        self.risk = CreatorRiskNormalizer()
        self.pattern = CreatorPatternMemory()
        self.network = CreatorNetwork()


    def confidence_engine(self, sample):

        if sample <= 1:
            return {
                "confidence": "LOW-MEDIUM",
                "quality": "EARLY DATA",
                "weight": 0.35
            }

        elif sample <= 5:
            return {
                "confidence": "MEDIUM",
                "quality": "LIMITED",
                "weight": 0.55
            }

        elif sample <= 20:
            return {
                "confidence": "MEDIUM-HIGH",
                "quality": "GOOD",
                "weight": 0.75
            }

        else:
            return {
                "confidence": "HIGH",
                "quality": "STRONG HISTORY",
                "weight": 0.90
            }


    def analyze(self, creator):

        alpha = self.alpha.analyze(creator)
        risk = self.risk.analyze(creator)
        pattern = self.pattern.analyze(creator)
        network = self.network.analyze(creator)


        sample = alpha.get(
            "total_token",
            0
        )


        confidence = self.confidence_engine(
            sample
        )


        alpha_score = alpha.get(
            "alpha_score",
            0
        )

        risk_score = risk.get(
            "risk_score",
            100
        )


        final_score = int(
            (
                alpha_score * 0.55
                +
                (100-risk_score) * 0.30
                +
                pattern.get("pattern_score",0)*0.15
            )
        )


        if final_score >= 70:
            decision = "ENTRY CANDIDATE"

        elif final_score >= 50:
            decision = "WATCH"

        else:
            decision = "AVOID"


        return {

            "creator": creator,

            "final_score": final_score,

            "decision": decision,

            "alpha_probability":
                alpha.get(
                    "alpha_probability",
                    0
                ),

            "rug_probability":
                risk.get(
                    "risk_score",
                    100
                ),

            "confidence":
                confidence["confidence"],

            "quality":
                confidence["quality"],

            "weight":
                confidence["weight"],

            "sample":
                sample,

            "signals": [

                "Alpha signal detected"
                if alpha_score > 60
                else
                "Weak alpha signal"

            ]

        }



if __name__ == "__main__":

    creator = input(
        "Creator Address : "
    )


    engine = CreatorIntelligenceV17()

    result = engine.analyze(
        creator
    )


    print()
    print("==============================")
    print(" CREATOR INTELLIGENCE V17 ")
    print("==============================")

    print(
        "Creator          :",
        result["creator"]
    )

    print(
        "Final Score      :",
        str(result["final_score"]) + "/100"
    )

    print(
        "Decision         :",
        result["decision"]
    )

    print("--------------------------------")

    print(
        "Alpha Probability :",
        str(result["alpha_probability"])+"%"
    )

    print(
        "Rug Probability   :",
        str(result["rug_probability"])+"%"
    )

    print("--------------------------------")

    print(
        "Confidence       :",
        result["confidence"]
    )

    print(
        "Data Quality     :",
        result["quality"]
    )

    print(
        "Sample Size      :",
        result["sample"]
    )

    print(
        "History Weight   :",
        result["weight"]
    )

    print("--------------------------------")

    print("SIGNALS")

    for s in result["signals"]:
        print("-",s)