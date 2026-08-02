from backend.analysis.creator_alpha_score import CreatorAlphaScore
from backend.analysis.creator_risk_normalizer import CreatorRiskNormalizer
from backend.analysis.creator_reliability import CreatorReliability
from backend.analysis.creator_network import CreatorNetwork



class CreatorIntelligenceV10:


    def __init__(self):

        self.alpha_engine = CreatorAlphaScore()

        self.risk_engine = CreatorRiskNormalizer()

        self.reliability_engine = CreatorReliability()

        self.network_engine = CreatorNetwork()



    # ==========================================
    # CREATOR INTELLIGENCE V10
    # ==========================================


    def analyze(self, creator):


        alpha = self.alpha_engine.analyze(
            creator
        )


        risk = self.risk_engine.analyze(
            creator
        )


        reliability = self.reliability_engine.analyze(
            creator
        )


        network = self.network_engine.analyze(
            creator
        )



        if not alpha or not risk:

            return None





        alpha_score = alpha.get(
            "alpha_score",
            0
        )



        risk_score = risk.get(
            "risk_score",
            100
        )



        reliability_score = reliability.get(
            "reliability_score",
            0
        ) if reliability else 0




        network_score = network.get(
            "network_score",
            0
        ) if network else 0





        # ======================================
        # FINAL SCORE
        #
        # Alpha       50%
        # Reliability 20%
        # Network     10%
        # Risk        20%
        #
        # ======================================


        final_score = round(

            (

                alpha_score * 0.50

                +

                reliability_score * 0.20

                +

                network_score * 0.10

                +

                (100 - risk_score) * 0.20

            )

        )



        # ======================================
        # TIER
        # ======================================


        if final_score >= 80:


            tier = "ALPHA CREATOR"


        elif final_score >= 65:


            tier = "EARLY PROMISING"


        elif final_score >= 40:


            tier = "WATCH LIST"


        else:


            tier = "AVOID CREATOR"





        # ======================================
        # CONFIDENCE
        # ======================================


        total_token = alpha.get(
            "total_token",
            0
        )



        if total_token >= 50:


            confidence = "HIGH"


        elif total_token >= 10:


            confidence = "MEDIUM"


        else:


            confidence = "LOW"





        # ======================================
        # REASONS
        # ======================================


        reasons = []



        if alpha.get("reasons"):


            reasons.extend(
                alpha["reasons"]
            )



        if risk.get("reasons"):


            reasons.extend(
                risk["reasons"]
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


            "alpha_score": alpha_score,


            "risk_score": risk_score,


            "risk_level": risk.get(
                "risk_level"
            ),


            "reliability_score": reliability_score,


            "network_score": network_score,


            "total_token": total_token,


            "highest_mc": alpha.get(
                "highest_mc",
                0
            ),


            "reasons": reasons

        }





    def close(self):


        self.alpha_engine.close()

        self.risk_engine.close()

        self.reliability_engine.close()

        self.network_engine.close()





# ==========================================
# TEST
# ==========================================


if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorIntelligenceV10()



    result = engine.analyze(
        creator
    )



    print()


    print("==============================")
    print(" CREATOR INTELLIGENCE V10 ")
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


        print("--------------------------------")


        print(
            f"Alpha Score      : {result['alpha_score']}"
        )


        print(
            f"Risk Score       : {result['risk_score']}"
        )


        print(
            f"Risk Level       : {result['risk_level']}"
        )


        print(
            f"Reliability      : {result['reliability_score']}"
        )


        print(
            f"Network          : {result['network_score']}"
        )


        print(
            f"Highest MC       : {result['highest_mc']:.2f}"
        )


        print("--------------------------------")


        print(
            "REASONS"
        )


        for r in result["reasons"]:


            print(
                "-",
                r
            )



    engine.close()