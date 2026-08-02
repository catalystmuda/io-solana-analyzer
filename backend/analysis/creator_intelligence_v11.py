from backend.analysis.creator_alpha_score import CreatorAlphaScore
from backend.analysis.creator_risk_normalizer import CreatorRiskNormalizer
from backend.analysis.creator_reliability import CreatorReliability
from backend.analysis.creator_network import CreatorNetwork
from backend.analysis.creator_temporal import CreatorTemporal



class CreatorIntelligenceV11:


    def __init__(self):

        self.alpha_engine = CreatorAlphaScore()

        self.risk_engine = CreatorRiskNormalizer()

        self.reliability_engine = CreatorReliability()

        self.network_engine = CreatorNetwork()

        self.temporal_engine = CreatorTemporal()



    # =====================================
    # CREATOR INTELLIGENCE V11
    # =====================================


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


        temporal = self.temporal_engine.analyze(
            creator
        )



        if not alpha:

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
        )


        network_score = network.get(
            "network_score",
            0
        )


        temporal_score = temporal.get(
            "temporal_score",
            0
        )



        # =====================================
        # FINAL AI SCORE
        # =====================================


        final_score = round(


            (alpha_score * 0.30)

            +

            ((100-risk_score) * 0.25)

            +

            (reliability_score * 0.15)

            +

            (network_score * 0.10)

            +

            (temporal_score * 0.20)


        )



        # =====================================
        # TIER
        # =====================================


        if final_score >= 75:

            tier = "EARLY PROMISING"


        elif final_score >= 55:

            tier = "WATCH LIST"


        elif final_score >= 35:

            tier = "HIGH RISK"


        else:

            tier = "AVOID CREATOR"




        # =====================================
        # CONFIDENCE
        # =====================================


        confidence = "LOW"


        total_token = alpha.get(
            "total_token",
            0
        )


        if total_token >= 10:

            confidence = "MEDIUM"


        if total_token >= 50:

            confidence = "HIGH"




        # =====================================
        # SIGNALS
        # =====================================


        reasons=[]



        if alpha_score >= 70:

            reasons.append(
                "Alpha signal detected"
            )


        if risk_score >= 70:

            reasons.append(
                "High risk pattern"
            )


        if reliability_score < 50:

            reasons.append(
                "Low creator reliability"
            )


        if temporal_score < 30:

            reasons.append(
                "Extreme launch frequency"
            )


        if network_score >= 50:

            reasons.append(
                "Creator network detected"
            )


        if not reasons:

            reasons.append(
                "No strong signal"
            )



        return {


            "creator": creator,


            "final_score": final_score,


            "tier": tier,


            "confidence": confidence,


            "alpha_score": alpha_score,


            "risk_score": risk_score,


            "reliability": reliability_score,


            "network": network_score,


            "temporal": temporal_score,


            "reasons": reasons

        }





    def close(self):


        self.alpha_engine.close()

        self.risk_engine.close()

        self.reliability_engine.close()

        self.network_engine.close()

        self.temporal_engine.close()





# =====================================
# TEST
# =====================================


if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorIntelligenceV11()



    result = engine.analyze(
        creator
    )



    print()

    print("==============================")
    print(" CREATOR INTELLIGENCE V11 ")
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
            f"Reliability      : {result['reliability']}"
        )


        print(
            f"Network          : {result['network']}"
        )


        print(
            f"Temporal         : {result['temporal']}"
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