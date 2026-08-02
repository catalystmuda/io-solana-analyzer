import sqlite3

from backend.analysis.creator_score import CreatorScore
from backend.analysis.creator_behavior import CreatorBehavior
from backend.analysis.creator_survival import CreatorSurvival



class CreatorIntelligence:



    def __init__(self):

        self.score_engine = CreatorScore()

        self.behavior_engine = CreatorBehavior()

        self.survival_engine = CreatorSurvival()



    # ======================================
    # MAIN AI ANALYSIS
    # ======================================


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



        if score is None:

            return None



        creator_score = score["creator_score"]

        pattern_score = score["pattern_score"]


        behavior_score = 0

        behavior_risk = 100


        if behavior:

            behavior_score = behavior.get(
                "behavior_score",
                0
            )

            behavior_risk = behavior.get(
                "behavior_risk",
                100
            )



        survival_score = 0


        if survival:

            survival_score = survival.get(
                "survival_score",
                0
            )



        # ==================================
        # FINAL AI SCORE
        # ==================================


        final_score = round(

            creator_score * 0.25 +

            pattern_score * 0.25 +

            behavior_score * 0.25 +

            survival_score * 0.25

        )



        reasons = []



        if behavior:

            reasons.extend(
                behavior.get(
                    "reasons",
                    []
                )
            )



        if survival:

            reasons.extend(
                survival.get(
                    "reasons",
                    []
                )
            )



        if score["avg_marketcap"] < 50:

            reasons.append(
                "Average MarketCap masih rendah"
            )



        if score["highest_marketcap"] < 100:

            reasons.append(
                "Belum ada marketcap besar"
            )



        # hapus duplikat

        reasons = list(
            dict.fromkeys(
                reasons
            )
        )



        if final_score >= 70:

            verdict = "LOW RISK CREATOR"


        elif final_score >= 45:

            verdict = "MEDIUM RISK CREATOR"


        else:

            verdict = "HIGH RISK CREATOR"



        return {


            "creator": creator,

            "final_score": final_score,

            "verdict": verdict,

            "confidence": score["confidence"],

            "creator_score": creator_score,

            "pattern_score": pattern_score,

            "behavior_score": behavior_score,

            "behavior_risk": behavior_risk,

            "survival_score": survival_score,

            "reasons": reasons

        }



    def close(self):

        self.score_engine.close()

        self.survival_engine.close()







if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorIntelligence()



    result = engine.analyze(
        creator
    )



    print()

    print(
        "========================================"
    )

    print(
        "      CREATOR INTELLIGENCE V2"
    )

    print(
        "========================================"
    )



    if result is None:

        print(
            "Creator tidak ditemukan"
        )


    else:


        print(
            f"Creator            : {result['creator']}"
        )


        print("----------------------------------------")


        print(
            f"Final AI Score     : {result['final_score']}/100"
        )


        print(
            f"Verdict            : {result['verdict']}"
        )


        print(
            f"Confidence         : {result['confidence']}"
        )


        print("----------------------------------------")


        print(
            f"Creator Score      : {result['creator_score']}/100"
        )


        print(
            f"Pattern Score      : {result['pattern_score']}/100"
        )


        print(
            f"Behavior Score     : {result['behavior_score']}/100"
        )


        print(
            f"Behavior Risk      : {result['behavior_risk']}/100"
        )


        print(
            f"Survival Score     : {result['survival_score']}/100"
        )


        print("----------------------------------------")


        print(
            "AI REASONS"
        )


        for r in result["reasons"]:

            print(
                "-",
                r
            )



    engine.close()