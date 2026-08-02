from backend.analysis.creator_alpha_score import CreatorAlphaScore
from backend.analysis.creator_risk_normalizer import CreatorRiskNormalizer
from backend.analysis.creator_pattern_memory import CreatorPatternMemory
from backend.analysis.creator_network import CreatorNetwork
from backend.analysis.creator_temporal import CreatorTemporal



class CreatorIntelligenceV19:


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



        sample_size = alpha.get(
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


        highest_mc = alpha.get(
            "highest_mc",
            0
        )


        breakout = alpha.get(
            "breakout",
            0
        )


        survivor = alpha.get(
            "survivor",
            0
        )



        # =============================
        # MARKET STRENGTH
        # =============================

        market_strength = min(
            100,
            int(highest_mc / 10)
        )



        # =============================
        # RAW SCORE
        # =============================

        raw_score = int(

            alpha_score * 0.40

            +

            (100-risk_score) * 0.20

            +

            pattern_score * 0.15

            +

            network_score * 0.10

            +

            temporal_score * 0.05

            +

            market_strength * 0.10

        )



        # =============================
        # EVIDENCE SYSTEM
        # =============================


        if sample_size <= 1:

            evidence_quality = "EARLY DATA"
            history_weight = 0.70


        elif sample_size <= 5:

            evidence_quality = "LIMITED HISTORY"
            history_weight = 0.80


        elif sample_size <= 20:

            evidence_quality = "GOOD HISTORY"
            history_weight = 0.90


        else:

            evidence_quality = "STRONG HISTORY"
            history_weight = 1.00



        evidence_score = int(

            raw_score *
            history_weight

        )



        # =============================
        # BONUS SIGNAL
        # =============================


        bonus = 0


        if breakout:

            bonus += 10


        if survivor:

            bonus += 5


        if pattern_score >= 80:

            bonus += 5



        final_score = min(

            100,

            evidence_score + bonus

        )



        # =============================
        # PROBABILITY
        # =============================


        alpha_probability = int(

            alpha_score *
            history_weight

            +

            bonus

        )


        alpha_probability = max(
            0,
            min(
                95,
                alpha_probability
            )
        )


        rug_probability = max(
            0,
            min(
                95,
                risk_score
            )
        )



        # =============================
        # DECISION
        # =============================


        if final_score >=90:

            decision = "ALPHA CREATOR"


        elif final_score >=75:

            decision = "ENTRY CANDIDATE"


        elif final_score >=60:

            decision = "WATCH LIST"


        elif final_score >=40:

            decision = "CAUTION"


        else:

            decision = "AVOID"



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


        if risk_score >=70:

            signals.append(
                "High risk creator"
            )


        if sample_size <=1:

            signals.append(
                "Limited creator history"
            )



        return {

            "creator": creator,

            "final_score": final_score,

            "decision": decision,

            "alpha_probability": alpha_probability,

            "rug_probability": rug_probability,

            "evidence_quality": evidence_quality,

            "history_weight": history_weight,

            "sample_size": sample_size,

            "market_strength": market_strength,

            "pattern_score": pattern_score,

            "network_score": network_score,

            "signals": signals

        }





if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    )


    engine = CreatorIntelligenceV19()


    result = engine.analyze(
        creator
    )


    print()

    print("==============================")
    print(" CREATOR INTELLIGENCE V19 ")
    print("==============================")


    for k,v in result.items():

        print(
            f"{k:<22}: {v}"
        )