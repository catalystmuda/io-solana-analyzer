from backend.analysis.creator_alpha_score import CreatorAlphaScore
from backend.analysis.creator_risk_normalizer import CreatorRiskNormalizer
from backend.analysis.creator_pattern_memory import CreatorPatternMemory
from backend.analysis.creator_network import CreatorNetwork
from backend.analysis.creator_temporal import CreatorTemporal



class CreatorIntelligenceV17_3:


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



        # ==============================
        # PROBABILITY CALIBRATION V17.3
        # ==============================


        alpha_probability = alpha_score


        rug_probability = risk_score



        # early creator adjustment

        if total_token <= 1:


            # reward evidence

            if breakout:

                alpha_probability += 10


            if survivor:

                alpha_probability += 5


            if highest_mc >= 500:

                alpha_probability += 5



            # uncertainty penalty

            alpha_probability -= 15

            rug_probability += 10



        elif total_token <= 5:


            alpha_probability -= 5

            rug_probability += 5



        alpha_probability = max(
            0,
            min(
                90,
                alpha_probability
            )
        )


        rug_probability = max(
            0,
            min(
                95,
                rug_probability
            )
        )



        # ==============================
        # STABILITY SCORE
        # ==============================


        stability = (

            pattern_score * 0.4

            +

            network_score * 0.3

            +

            temporal_score * 0.3

        )


        stability = int(
            stability
        )



        market_strength = min(
            100,
            int(
                highest_mc / 10
            )
        )



        # ==============================
        # FINAL SCORE
        # ==============================


        final_score = int(

            alpha_probability * 0.35

            +

            (100-rug_probability) * 0.25

            +

            stability * 0.20

            +

            market_strength * 0.20

        )



        if final_score >=75:

            decision="ENTRY CANDIDATE"

        elif final_score >=50:

            decision="WATCH LIST"

        else:

            decision="AVOID"



        if total_token <=1:

            confidence="LOW-MEDIUM"

        elif total_token <10:

            confidence="MEDIUM"

        else:

            confidence="HIGH"



        signals=[]


        if breakout:

            signals.append(
                "Breakout token detected"
            )


        if survivor:

            signals.append(
                "Survival token detected"
            )


        if pattern_score>=70:

            signals.append(
                "Clean creator pattern"
            )


        if rug_probability>=70:

            signals.append(
                "High risk creator"
            )



        return {


            "creator":creator,

            "final_score":final_score,

            "decision":decision,


            "alpha_probability":
                alpha_probability,


            "rug_probability":
                rug_probability,


            "confidence":
                confidence,


            "history_confidence":
                confidence,


            "market_strength":
                market_strength,


            "creator_stability":
                stability,


            "sample_size":
                total_token,


            "signals":
                signals

        }





if __name__=="__main__":


    creator=input(
        "Creator Address : "
    )


    engine=CreatorIntelligenceV17_3()


    result=engine.analyze(
        creator
    )


    print()

    print("==============================")

    print(" CREATOR INTELLIGENCE V17.3 ")

    print("==============================")


    for key,value in result.items():

        print(
            f"{key:<22}: {value}"
        )
        