from backend.analysis.creator_intelligence_v8 import CreatorIntelligenceV8
from backend.analysis.creator_alpha_score import CreatorAlphaScore



class CreatorIntelligenceV9:


    def __init__(self):

        self.intelligence_engine = CreatorIntelligenceV8()

        self.alpha_engine = CreatorAlphaScore()



    # ==========================================
    # ANALYZE CREATOR V9
    # ==========================================


    def analyze(self, creator):


        intelligence = self.intelligence_engine.analyze(
            creator
        )


        alpha = self.alpha_engine.analyze(
            creator
        )



        if intelligence is None or alpha is None:

            return None



        # ======================================
        # COMPATIBILITY V8
        # ======================================


        risk_score = intelligence.get(
            "final_score",
            intelligence.get(
                "ai_score",
                intelligence.get(
                    "score",
                    0
                )
            )
        )



        alpha_score = alpha.get(
            "alpha_score",
            0
        )



        total_token = alpha.get(
            "total_token",
            0
        )



        # ======================================
        # CONFIDENCE WEIGHT
        # ======================================


        if total_token >= 50:

            weight = 1.0


        elif total_token >= 10:

            weight = 0.85


        else:

            weight = 0.65





        # ======================================
        # FINAL AI SCORE
        #
        # Risk Engine 40%
        # Alpha Engine 60%
        #
        # ======================================


        final_score = round(

            (

                risk_score * 0.4

                +

                alpha_score * 0.6

            )

            *

            weight

        )





        # ======================================
        # TIER
        # ======================================


        if final_score >= 80:

            tier = "ALPHA CREATOR"


        elif final_score >= 60:

            tier = "EARLY PROMISING"


        elif final_score >= 40:

            tier = "WATCH LIST"


        else:

            tier = "HIGH RISK CREATOR"





        # ======================================
        # CONFIDENCE
        # ======================================


        if total_token >= 20:

            confidence = "HIGH"


        elif total_token >= 5:

            confidence = "MEDIUM"


        else:

            confidence = "LOW"





        # ======================================
        # MERGE REASONS
        # ======================================


        reasons = []


        if "reasons" in alpha:

            reasons.extend(
                alpha["reasons"]
            )


        if "reasons" in intelligence:

            reasons.extend(
                intelligence["reasons"]
            )



        reasons = list(
            dict.fromkeys(
                reasons
            )
        )





        return {


            "creator": creator,


            "final_score": final_score,


            "tier": tier,


            "confidence": confidence,


            "weight": weight,


            "risk_score": risk_score,


            "alpha_score": alpha_score,


            "survival": alpha.get(
                "survival",
                0
            ),


            "breakout": alpha.get(
                "breakout",
                0
            ),


            "highest_mc": alpha.get(
                "highest_mc",
                0
            ),


            "total_token": total_token,


            "reasons": reasons

        }





    def close(self):


        self.intelligence_engine.close()

        self.alpha_engine.close()





# ==========================================
# TEST
# ==========================================


if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorIntelligenceV9()



    result = engine.analyze(
        creator
    )



    print()


    print("==============================")
    print(" CREATOR INTELLIGENCE V9 ")
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
            f"Final Score      : {result['final_score']}/100"
        )


        print(
            f"Tier             : {result['tier']}"
        )


        print(
            f"Confidence       : {result['confidence']}"
        )


        print(
            f"Weight           : {result['weight']}"
        )


        print("--------------------------------")


        print(
            f"Risk Score       : {result['risk_score']}"
        )


        print(
            f"Alpha Score      : {result['alpha_score']}"
        )


        print(
            f"Survival         : {result['survival']}"
        )


        print(
            f"Breakout         : {result['breakout']}"
        )


        print(
            f"Highest MC       : {result['highest_mc']:.2f}"
        )


        print("--------------------------------")


        print(
            "SIGNALS"
        )


        for r in result["reasons"]:

            print(
                "-",
                r
            )



    engine.close()