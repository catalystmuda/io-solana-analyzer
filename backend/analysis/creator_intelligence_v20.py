from backend.analysis.creator_alpha_score import CreatorAlphaScore
from backend.analysis.creator_risk_normalizer import CreatorRiskNormalizer
from backend.analysis.creator_pattern_memory import CreatorPatternMemory
from backend.analysis.creator_network import CreatorNetwork
from backend.analysis.creator_temporal import CreatorTemporal


class CreatorIntelligenceV20:


    def __init__(self):

        self.alpha_engine = CreatorAlphaScore()
        self.risk_engine = CreatorRiskNormalizer()
        self.pattern_engine = CreatorPatternMemory()
        self.network_engine = CreatorNetwork()
        self.temporal_engine = CreatorTemporal()



    def safe_run(self, engine, creator):

        try:

            if hasattr(engine, "analyze"):

                result = engine.analyze(
                    creator
                )

                if isinstance(result, dict):
                    return result


            if hasattr(engine, "calculate"):

                result = engine.calculate(
                    creator
                )

                if isinstance(result, dict):
                    return result


        except Exception:

            pass


        return {}



    def analyze(self, creator):


        alpha = self.safe_run(
            self.alpha_engine,
            creator
        )

        risk = self.safe_run(
            self.risk_engine,
            creator
        )

        pattern = self.safe_run(
            self.pattern_engine,
            creator
        )

        network = self.safe_run(
            self.network_engine,
            creator
        )

        temporal = self.safe_run(
            self.temporal_engine,
            creator
        )



        sample = alpha.get(
            "total_token",
            0
        )

        alpha_score = alpha.get(
            "alpha_score",
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


        breakout = alpha.get(
            "breakout",
            0
        )

        survivor = alpha.get(
            "survivor",
            0
        )

        highest_mc = alpha.get(
            "highest_mc",
            0
        )



        market_strength = min(
            100,
            int(highest_mc / 10)
        )



        # =========================
        # BASE SCORE
        # =========================


        base_score = int(

            alpha_score * 0.40

            +

            (100-risk_score) * 0.20

            +

            pattern_score * 0.20

            +

            network_score * 0.10

            +

            market_strength * 0.10

        )



        # =========================
        # HISTORY CONTROL
        # =========================


        if sample <= 1:

            history_weight = 0.75
            evidence = "EARLY DATA"

        elif sample <= 5:

            history_weight = 0.85
            evidence = "LIMITED HISTORY"

        elif sample <=20:

            history_weight = 0.95
            evidence = "GOOD HISTORY"

        else:

            history_weight = 1.0
            evidence = "STRONG HISTORY"



        score = int(
            base_score * history_weight
        )



        # =========================
        # EARLY ALPHA BOOST
        # =========================


        early_alpha_boost = 0


        if (

            sample <= 2

            and breakout

            and risk_score < 30

            and pattern_score >= 80

        ):

            early_alpha_boost = 20



        if survivor:

            early_alpha_boost += 5



        final_score = min(

            100,

            score + early_alpha_boost

        )



        # =========================
        # PROBABILITY
        # =========================


        alpha_probability = min(

            95,

            int(

                alpha_score

                +

                early_alpha_boost

            )

        )


        rug_probability = risk_score



        # =========================
        # DECISION
        # =========================


        if final_score >=85:

            decision = "ENTRY CANDIDATE"


        elif final_score >=65:

            decision = "WATCH LIST"


        else:

            decision = "AVOID"



        if final_score >=85:

            grade="A"

        elif final_score >=70:

            grade="B"

        elif final_score >=50:

            grade="C"

        else:

            grade="D"



        signals=[]


        if breakout:

            signals.append(
                "Breakout token detected"
            )


        if survivor:

            signals.append(
                "Survival token detected"
            )


        if pattern_score >=80:

            signals.append(
                "Clean creator pattern"
            )


        if early_alpha_boost:

            signals.append(
                "Early alpha boost applied"
            )


        if risk_score >=70:

            signals.append(
                "High risk creator"
            )


        if sample <=1:

            signals.append(
                "Limited history"
            )



        return {

            "creator":creator,

            "final_score":final_score,

            "decision":decision,

            "grade":grade,

            "alpha_probability":alpha_probability,

            "rug_probability":rug_probability,

            "evidence":evidence,

            "sample_size":sample,

            "history_weight":history_weight,

            "early_alpha_boost":early_alpha_boost,

            "market_strength":market_strength,

            "pattern_score":pattern_score,

            "network_score":network_score,

            "signals":signals

        }




if __name__=="__main__":


    creator=input(
        "Creator Address : "
    )


    engine=CreatorIntelligenceV20()


    result=engine.analyze(
        creator
    )


    print()

    print("==============================")
    print(" CREATOR INTELLIGENCE V20 ")
    print("==============================")


    for k,v in result.items():

        print(
            f"{k:<22}: {v}"
        )