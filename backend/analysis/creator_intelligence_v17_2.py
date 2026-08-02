from backend.analysis.creator_alpha_score import CreatorAlphaScore
from backend.analysis.creator_risk_normalizer import CreatorRiskNormalizer
from backend.analysis.creator_pattern_memory import CreatorPatternMemory
from backend.analysis.creator_network import CreatorNetwork
from backend.analysis.creator_temporal import CreatorTemporal



class CreatorIntelligenceV17_2:


    def __init__(self):

        self.alpha = CreatorAlphaScore()
        self.risk = CreatorRiskNormalizer()
        self.pattern = CreatorPatternMemory()
        self.network = CreatorNetwork()
        self.temporal = CreatorTemporal()



    def safe_analyze(self, engine, creator):

        if hasattr(engine, "analyze"):

            return engine.analyze(
                creator
            )

        return {}



    def analyze(self, creator):


        alpha = self.safe_analyze(
            self.alpha,
            creator
        )


        risk = self.safe_analyze(
            self.risk,
            creator
        )


        pattern = self.safe_analyze(
            self.pattern,
            creator
        )


        network = self.safe_analyze(
            self.network,
            creator
        )


        temporal = self.safe_analyze(
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
            alpha.get(
                "survivor_count",
                0
            )
        )


        breakout = alpha.get(
            "breakout",
            alpha.get(
                "breakout_count",
                0
            )
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
        # PROBABILITY CALIBRATION
        # ==========================


        alpha_probability = alpha_score


        rug_probability = risk_score



        # early creator bonus

        if total_token <= 2:


            if breakout >= 1:

                alpha_probability += 15


            if highest_mc >= 500:

                alpha_probability += 10


            rug_probability -= 20



        alpha_probability = min(
            95,
            max(
                0,
                alpha_probability
            )
        )


        rug_probability = min(
            99,
            max(
                0,
                rug_probability
            )
        )



        # ==========================
        # FINAL SCORE
        # ==========================


        score = (

            alpha_probability * 0.35

            +

            (100-rug_probability) * 0.25

            +

            pattern_score * 0.20

            +

            network_score * 0.10

            +

            temporal_score * 0.10

        )


        final_score = int(score)



        if final_score >= 75:

            decision = "ENTRY CANDIDATE"

        elif final_score >=50:

            decision = "WATCH LIST"

        else:

            decision = "AVOID"



        if total_token <= 1:

            confidence = "LOW-MEDIUM"

        elif total_token < 10:

            confidence = "MEDIUM"

        else:

            confidence = "HIGH"



        signals=[]


        if breakout:

            signals.append(
                "Breakout token detected"
            )


        if survivor:

            signals.append(
                "Survival token detected"
            )


        if pattern_score >=70:

            signals.append(
                "Clean creator pattern"
            )


        if rug_probability >=70:

            signals.append(
                "High risk creator"
            )



        return {


            "creator":creator,

            "final_score":final_score,

            "decision":decision,

            "alpha_probability":alpha_probability,

            "rug_probability":rug_probability,

            "confidence":confidence,

            "sample_size":total_token,

            "signals":signals

        }




if __name__=="__main__":


    creator=input(
        "Creator Address : "
    )


    engine=CreatorIntelligenceV17_2()


    result=engine.analyze(
        creator
    )


    print()

    print("==============================")

    print(" CREATOR INTELLIGENCE V17.2 ")

    print("==============================")


    for key,value in result.items():

        print(
            f"{key:<20}: {value}"
        )