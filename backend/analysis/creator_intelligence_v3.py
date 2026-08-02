from backend.analysis.creator_score import CreatorScore
from backend.analysis.creator_behavior import CreatorBehavior
from backend.analysis.creator_survival import CreatorSurvival
from backend.analysis.creator_reliability import CreatorReliability



class CreatorIntelligenceV3:


    def __init__(self):

        self.score_engine = CreatorScore()

        self.behavior_engine = CreatorBehavior()

        self.survival_engine = CreatorSurvival()

        self.reliability_engine = CreatorReliability()



    # =====================================
    # ANALYZE CREATOR
    # =====================================

    def analyze(self, creator):


        score = self.score_engine.calculate(
            creator
        )


        behavior = self.behavior_engine.analyze(
            creator
        )


        survival = self.survival_engine.calculate(
            creator
        )


        reliability = self.reliability_engine.calculate(
            creator
        )


        if not score:

            return None



        final_score = round(

            score["creator_score"] * 0.25 +

            score["pattern_score"] * 0.15 +

            behavior["behavior_score"] * 0.15 +

            survival["survival_score"] * 0.20 +

            reliability["reliability_score"] * 0.25

        )



        reasons = []



        if behavior["behavior_risk"] >= 70:

            reasons.append(
                "High risk behavior detected"
            )


        if survival["survival_score"] < 30:

            reasons.append(
                "Low token survival"
            )


        if reliability["reliability_score"] < 50:

            reasons.append(
                "Low creator reliability"
            )


        if reliability["total_token"] < 5:

            reasons.append(
                "Limited creator history"
            )



        if final_score >= 75:

            verdict = "ALPHA CREATOR"

        elif final_score >= 50:

            verdict = "MEDIUM CREATOR"

        else:

            verdict = "HIGH RISK CREATOR"



        return {


            "creator": creator,

            "final_score": final_score,

            "verdict": verdict,

            "creator_score": score["creator_score"],

            "pattern_score": score["pattern_score"],

            "behavior_score": behavior["behavior_score"],

            "behavior_risk": behavior["behavior_risk"],

            "survival_score": survival["survival_score"],

            "reliability_score": reliability["reliability_score"],

            "reasons": reasons

        }



    def close(self):

        self.score_engine.close()

        self.reliability_engine.close()





# =====================================
# TEST
# =====================================

if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorIntelligenceV3()


    result = engine.analyze(
        creator
    )



    print()

    print("==============================")
    print(" CREATOR INTELLIGENCE V3")
    print("==============================")


    if result is None:

        print(
            "Creator tidak ditemukan"
        )


    else:


        print(
            f"Creator              : {result['creator']}"
        )

        print("--------------------------------")


        print(
            f"Final Score          : {result['final_score']}/100"
        )


        print(
            f"Verdict              : {result['verdict']}"
        )


        print("--------------------------------")


        print(
            f"Creator Score        : {result['creator_score']}"
        )


        print(
            f"Pattern Score        : {result['pattern_score']}"
        )


        print(
            f"Behavior Score       : {result['behavior_score']}"
        )


        print(
            f"Behavior Risk        : {result['behavior_risk']}"
        )


        print(
            f"Survival Score       : {result['survival_score']}"
        )


        print(
            f"Reliability Score    : {result['reliability_score']}"
        )


        print("--------------------------------")


        print("REASONS")

        for r in result["reasons"]:

            print("-", r)



    engine.close()