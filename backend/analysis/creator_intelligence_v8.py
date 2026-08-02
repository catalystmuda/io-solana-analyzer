from backend.analysis.creator_score import CreatorScore
from backend.analysis.creator_behavior import CreatorBehavior
from backend.analysis.creator_survival import CreatorSurvival
from backend.analysis.creator_reliability import CreatorReliability
from backend.analysis.creator_confidence import CreatorConfidence
from backend.analysis.creator_network import CreatorNetwork



class CreatorIntelligenceV8:


    def __init__(self):

        self.score_engine = CreatorScore()

        self.behavior_engine = CreatorBehavior()

        self.survival_engine = CreatorSurvival()

        self.reliability_engine = CreatorReliability()

        self.confidence_engine = CreatorConfidence()

        self.network_engine = CreatorNetwork()



    # =====================================
    # FULL CREATOR ANALYSIS V8
    # =====================================

    def analyze(self, creator):


        score = self.score_engine.calculate(
            creator
        )


        behavior = self.behavior_engine.analyze(
            creator
        )


        survival = self.survival_engine.analyze(
            creator
        )


        reliability = self.reliability_engine.analyze(
            creator
        )


        confidence = self.confidence_engine.analyze(
            creator
        )


        network = self.network_engine.analyze(
            creator
        )



        if not score:

            return None



        final_score = round(

            score["creator_score"] * 0.20 +

            score["pattern_score"] * 0.15 +

            behavior["behavior_score"] * 0.10 +

            survival["survival_score"] * 0.20 +

            reliability["reliability_score"] * 0.15 +

            confidence["confidence_score"] * 0.10 +

            network["network_score"] * 0.10

        )



        reasons = []



        reasons += behavior["reasons"]


        reasons += survival["reasons"]


        reasons += reliability.get(
            "reasons",
            []
        )


        reasons += network["reasons"]



        if final_score >= 75:

            tier = "ALPHA CREATOR"


        elif final_score >= 50:

            tier = "PROMISING CREATOR"


        else:

            tier = "HIGH RISK CREATOR"



        return {


            "creator": creator,

            "ai_score": final_score,

            "tier": tier,


            "creator_score":
            score["creator_score"],


            "pattern_score":
            score["pattern_score"],


            "behavior_score":
            behavior["behavior_score"],


            "survival_score":
            survival["survival_score"],


            "reliability_score":
            reliability["reliability_score"],


            "confidence_score":
            confidence["confidence_score"],


            "network_score":
            network["network_score"],


            "reasons":
            list(set(reasons))

        }



    def close(self):

        self.score_engine.close()

        self.reliability_engine.close()

        self.confidence_engine.close()

        self.network_engine.close()





# =====================================
# TEST
# =====================================


if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorIntelligenceV8()


    result = engine.analyze(
        creator
    )



    print()

    print("==============================")
    print(" CREATOR INTELLIGENCE V8 ")
    print("==============================")


    if result is None:

        print(
            "Creator tidak ditemukan"
        )


    else:


        print(
            f"Creator          : {result['creator']}"
        )

        print("--------------------------------")


        print(
            f"AI Score         : {result['ai_score']}/100"
        )


        print(
            f"Tier             : {result['tier']}"
        )


        print("--------------------------------")


        print(
            f"Creator Score    : {result['creator_score']}"
        )


        print(
            f"Pattern Score    : {result['pattern_score']}"
        )


        print(
            f"Behavior Score   : {result['behavior_score']}"
        )


        print(
            f"Survival Score   : {result['survival_score']}"
        )


        print(
            f"Reliability      : {result['reliability_score']}"
        )


        print(
            f"Confidence       : {result['confidence_score']}"
        )


        print(
            f"Network          : {result['network_score']}"
        )


        print("--------------------------------")

        print("REASONS")


        for r in result["reasons"]:

            print(
                "-",
                r
            )



    engine.close()