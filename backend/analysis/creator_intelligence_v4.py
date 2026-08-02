from backend.analysis.creator_score import CreatorScore
from backend.analysis.creator_behavior import CreatorBehavior
from backend.analysis.creator_survival import CreatorSurvival
from backend.analysis.creator_reliability import CreatorReliability


class CreatorIntelligenceV4:


    def __init__(self):

        self.score_engine = CreatorScore()
        self.behavior_engine = CreatorBehavior()
        self.survival_engine = CreatorSurvival()
        self.reliability_engine = CreatorReliability()



    # =====================================
    # CREATOR INTELLIGENCE V4
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



        if not score or not behavior or not survival or not reliability:

            return None



        # =====================================
        # MANIPULATION DETECTION
        # =====================================

        manipulation_score = 100


        reasons = []



        # Mass launch

        if behavior["behavior_risk"] >= 70:

            manipulation_score -= 30

            reasons.append(
                "Mass launch pattern detected"
            )



        # Duplicate pattern

        if score["pattern_score"] < 50:

            manipulation_score -= 20

            reasons.append(
                "Token fingerprint terlalu mirip"
            )



        # Survival rendah

        if survival["survival_score"] < 30:

            manipulation_score -= 20

            reasons.append(
                "Low survival history"
            )



        # Reliability rendah

        if reliability["reliability_score"] < 50:

            manipulation_score -= 20

            reasons.append(
                "Low creator reliability"
            )



        manipulation_score = max(
            manipulation_score,
            0
        )



        # =====================================
        # FINAL AI SCORE
        # =====================================


        final_score = round(

            score["creator_score"] * 0.25 +

            score["pattern_score"] * 0.15 +

            behavior["behavior_score"] * 0.15 +

            survival["survival_score"] * 0.20 +

            reliability["reliability_score"] * 0.15 +

            manipulation_score * 0.10

        )



        final_score = max(
            min(final_score,100),
            0
        )



        # =====================================
        # VERDICT
        # =====================================


        if final_score >= 80:

            verdict = "ALPHA CREATOR"


        elif final_score >= 60:

            verdict = "PROMISING CREATOR"


        elif final_score >= 40:

            verdict = "NEUTRAL CREATOR"


        else:

            verdict = "HIGH RISK CREATOR"




        # =====================================
        # CONFIDENCE
        # =====================================


        if score["total_token"] >= 50:

            confidence = "HIGH"


        elif score["total_token"] >= 10:

            confidence = "MEDIUM"


        else:

            confidence = "LOW"




        if not reasons:

            reasons.append(
                "Creator pattern terlihat normal"
            )



        return {


            "creator": creator,


            "final_score": final_score,


            "verdict": verdict,


            "confidence": confidence,


            "creator_score": score["creator_score"],


            "pattern_score": score["pattern_score"],


            "behavior_score": behavior["behavior_score"],


            "behavior_risk": behavior["behavior_risk"],


            "survival_score": survival["survival_score"],


            "reliability_score": reliability["reliability_score"],


            "manipulation_score": manipulation_score,


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



    engine = CreatorIntelligenceV4()


    result = engine.analyze(
        creator
    )



    print()

    print("==============================")
    print(" CREATOR INTELLIGENCE V4")
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


        print(
            f"Confidence           : {result['confidence']}"
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


        print(
            f"Manipulation Score   : {result['manipulation_score']}"
        )


        print("--------------------------------")


        print(
            "AI REASONS"
        )


        for reason in result["reasons"]:

            print(
                "-",
                reason
            )



    engine.close()