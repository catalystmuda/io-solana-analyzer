from backend.analysis.creator_alpha_score import CreatorAlphaScore
from backend.analysis.creator_risk_normalizer import CreatorRiskNormalizer
from backend.analysis.creator_pattern_memory import CreatorPatternMemory
from backend.analysis.creator_network import CreatorNetwork
from backend.analysis.creator_temporal import CreatorTemporal



class CreatorIntelligenceV18:


    def __init__(self):

        self.alpha = CreatorAlphaScore()
        self.risk = CreatorRiskNormalizer()
        self.pattern = CreatorPatternMemory()
        self.network = CreatorNetwork()
        self.temporal = CreatorTemporal()



    def run(self, engine, creator):

        if hasattr(engine, "analyze"):

            return engine.analyze(
                creator
            )

        return {}



    def analyze(self, creator):


        alpha = self.run(
            self.alpha,
            creator
        )


        risk = self.run(
            self.risk,
            creator
        )


        pattern = self.run(
            self.pattern,
            creator
        )


        network = self.run(
            self.network,
            creator
        )


        temporal = self.run(
            self.temporal,
            creator
        )



        total_token = alpha.get(
            "total_token",
            0
        )


        alpha_score = alpha.get(
            "alpha_score",
            0
        )


        survivor = alpha.get(
            "survivor",
            0
        )


        breakout = alpha.get(
            "breakout",
            0
        )


        highest_mc = alpha.get(
            "highest_mc",
            0
        )


        risk_score = risk.get(
            "risk_score",
            50
        )


        pattern_score = pattern.get(
            "pattern_score",
            50
        )


        network_score = network.get(
            "network_score",
            50
        )


        temporal_score = temporal.get(
            "temporal_score",
            50
        )



        # ==========================
        # RAW SCORE
        # ==========================


        raw_score = int(

            alpha_score * 0.35

            +

            (100-risk_score) * 0.25

            +

            pattern_score * 0.20

            +

            network_score * 0.10

            +

            temporal_score * 0.10

        )



        # ==========================
        # HISTORY WEIGHT
        # ==========================


        if total_token <=1:

            history_weight = 0.45

        elif total_token <=5:

            history_weight = 0.65

        elif total_token <=20:

            history_weight = 0.80

        else:

            history_weight = 0.95



        evidence_score = int(

            raw_score * history_weight

        )



        # ==========================
        # ALPHA BONUS
        # ==========================


        bonus = 0


        if breakout:

            bonus += 20


        if survivor:

            bonus += 10


        if pattern_score >=80:

            bonus += 10



        adjusted_score = min(

            100,

            evidence_score + bonus

        )



        # ==========================
        # PROBABILITY
        # ==========================


        alpha_probability = int(

            alpha_score * history_weight

            +

            bonus

        )


        rug_probability = risk_score



        alpha_probability = max(
            0,
            min(
                90,
                alpha_probability
            )
        )



        # ==========================
        # DECISION
        # ==========================


        if adjusted_score >=75:

            decision="EARLY ENTRY"


        elif adjusted_score >=55:

            decision="WATCH LIST"


        else:

            decision="AVOID"



        if total_token <=1:

            confidence="LOW"

        elif total_token <10:

            confidence="MEDIUM"

        else:

            confidence="HIGH"



        reasons=[]


        if breakout:

            reasons.append(
                "Breakout detected"
            )


        if survivor:

            reasons.append(
                "Survival token detected"
            )


        if pattern_score>=80:

            reasons.append(
                "Clean creator pattern"
            )


        if total_token<=1:

            reasons.append(
                "Limited creator history"
            )


        if risk_score>=70:

            reasons.append(
                "High risk creator"
            )



        return {


            "creator":creator,

            "raw_score":raw_score,

            "evidence_score":evidence_score,

            "adjusted_score":adjusted_score,

            "decision":decision,

            "alpha_probability":alpha_probability,

            "rug_probability":rug_probability,

            "confidence":confidence,

            "history_weight":history_weight,

            "sample_size":total_token,

            "reasons":reasons

        }





if __name__=="__main__":


    creator=input(
        "Creator Address : "
    )


    engine=CreatorIntelligenceV18()


    result=engine.analyze(
        creator
    )


    print()

    print("==============================")

    print(" CREATOR INTELLIGENCE V18 ")

    print("==============================")


    for key,value in result.items():

        print(
            f"{key:<22}: {value}"
        )