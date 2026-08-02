from backend.analysis.creator_probability import CreatorProbability
from backend.analysis.creator_alpha_score import CreatorAlphaScore
from backend.analysis.creator_risk_normalizer import CreatorRiskNormalizer
from backend.analysis.creator_pattern_memory import CreatorPatternMemory
from backend.analysis.creator_network import CreatorNetwork
from backend.analysis.creator_temporal import CreatorTemporal



class CreatorIntelligenceV17_1:


    def __init__(self):

        self.probability = CreatorProbability()
        self.alpha = CreatorAlphaScore()
        self.risk = CreatorRiskNormalizer()
        self.pattern = CreatorPatternMemory()
        self.network = CreatorNetwork()
        self.temporal = CreatorTemporal()



    def analyze_engine(self, engine, creator):

        if hasattr(engine,"analyze"):

            return engine.analyze(
                creator
            )

        return {}



    def analyze(self, creator):


        alpha = self.analyze_engine(
            self.alpha,
            creator
        )


        risk = self.analyze_engine(
            self.risk,
            creator
        )


        pattern = self.analyze_engine(
            self.pattern,
            creator
        )


        network = self.analyze_engine(
            self.network,
            creator
        )


        temporal = self.analyze_engine(
            self.temporal,
            creator
        )



        # DATA UNTUK PROBABILITY ENGINE

        probability_data = {

            "alpha_score":
                alpha.get(
                    "alpha_score",
                    0
                ),


            "risk_score":
                risk.get(
                    "risk_score",
                    0
                ),


            "survival":
                alpha.get(
                    "survivor",
                    0
                ),


            "breakout":
                alpha.get(
                    "breakout",
                    0
                ),


            "total_token":
                alpha.get(
                    "total_token",
                    0
                )
        }



        # probability menerima DATA

        if hasattr(
            self.probability,
            "calculate"
        ):

            probability = self.probability.calculate(
                probability_data
            )

        else:

            probability = {}



        alpha_probability = probability.get(
            "alpha_probability",
            0
        )


        rug_probability = probability.get(
            "rug_probability",
            risk.get(
                "risk_score",
                0
            )
        )



        alpha_score = alpha.get(
            "alpha_score",
            0
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


        sample = alpha.get(
            "total_token",
            0
        )



        if sample <= 1:

            confidence="LOW-MEDIUM"
            quality="EARLY DATA"

        elif sample <=10:

            confidence="MEDIUM"
            quality="LIMITED"

        else:

            confidence="HIGH"
            quality="STRONG HISTORY"



        final_score = int(

            alpha_score * 0.40

            +

            pattern_score * 0.20

            +

            network_score * 0.15

            +

            temporal_score * 0.10

            +

            (100-rug_probability)*0.15

        )



        if final_score >=75:

            decision="ENTRY CANDIDATE"

        elif final_score >=50:

            decision="WATCH LIST"

        else:

            decision="AVOID"



        return {

            "creator":creator,

            "final_score":final_score,

            "decision":decision,

            "alpha_probability":alpha_probability,

            "rug_probability":rug_probability,

            "confidence":confidence,

            "quality":quality,

            "sample":sample

        }





if __name__=="__main__":


    creator=input(
        "Creator Address : "
    )


    engine=CreatorIntelligenceV17_1()


    result=engine.analyze(
        creator
    )


    print()

    print("==============================")

    print(" CREATOR INTELLIGENCE V17.1 FIX ")

    print("==============================")


    for key,value in result.items():

        print(
            f"{key:<20}: {value}"
        )