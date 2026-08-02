from backend.analysis.creator_score import CreatorScore
from backend.analysis.creator_behavior import CreatorBehavior
from backend.analysis.creator_survival import CreatorSurvival
from backend.analysis.creator_reliability import CreatorReliability
from backend.analysis.creator_confidence import CreatorConfidence



class CreatorIntelligenceV5:


    def __init__(self):

        self.score_engine = CreatorScore()
        self.behavior_engine = CreatorBehavior()
        self.survival_engine = CreatorSurvival()
        self.reliability_engine = CreatorReliability()
        self.confidence_engine = CreatorConfidence()



    # =====================================
    # ANALYZE CREATOR V5
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


        reliability = self.reliability_engine.calculate(
            creator
        )


        confidence = self.confidence_engine.analyze(
            creator
        )



        if not score or not behavior or not survival or not reliability or not confidence:

            return None



        base_score = (

            score["creator_score"] * 0.25 +

            score["pattern_score"] * 0.15 +

            behavior["behavior_score"] * 0.15 +

            survival["survival_score"] * 0.20 +

            reliability["reliability_score"] * 0.25

        )



        final_score = round(

            base_score * confidence["weight"]

        )



        reasons = []



        if behavior["behavior_risk"] >= 70:

            reasons.append(
                "High risk behavior"
            )



        if survival["survival_score"] < 30:

            reasons.append(
                "Low survival"
            )



        if confidence["confidence"] == "LOW":

            reasons.append(
                "Limited creator history"
            )



        if not reasons:

            reasons.append(
                "Healthy creator profile"
            )



        if final_score >= 80:

            verdict = "ALPHA CREATOR"


        elif final_score >= 60:

            verdict = "PROMISING CREATOR"


        elif final_score >= 40:

            verdict = "NEUTRAL CREATOR"


        else:

            verdict = "HIGH RISK CREATOR"



        return {

            "creator": creator,

            "final_score": final_score,

            "verdict": verdict,

            "confidence": confidence["confidence"],

            "confidence_weight": confidence["weight"],

            "creator_score": score["creator_score"],

            "pattern_score": score["pattern_score"],

            "behavior_score": behavior["behavior_score"],

            "survival_score": survival["survival_score"],

            "reliability_score": reliability["reliability_score"],

            "reasons": reasons

        }



    def close(self):

        self.score_engine.close()
        self.reliability_engine.close()
        self.confidence_engine.close()





if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()


    engine = CreatorIntelligenceV5()


    result = engine.analyze(
        creator
    )


    print()

    print("==============================")
    print(" CREATOR INTELLIGENCE V5 ")
    print("==============================")


    if result:


        print(
            f"Creator          : {result['creator']}"
        )

        print("--------------------------------")

        print(
            f"Final Score      : {result['final_score']}/100"
        )

        print(
            f"Verdict          : {result['verdict']}"
        )

        print(
            f"Confidence       : {result['confidence']}"
        )

        print(
            f"Weight           : {result['confidence_weight']}"
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

        print("--------------------------------")

        print("REASONS")

        for r in result["reasons"]:

            print("-", r)


    else:

        print(
            "Creator tidak ditemukan"
        )


    engine.close()