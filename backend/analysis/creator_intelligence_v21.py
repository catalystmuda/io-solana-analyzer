from backend.analysis.creator_alpha_score import CreatorAlphaScore
from backend.analysis.creator_risk_normalizer import CreatorRiskNormalizer
from backend.analysis.creator_pattern_memory import CreatorPatternMemory
from backend.analysis.creator_network import CreatorNetwork
from backend.analysis.creator_temporal import CreatorTemporal


class CreatorIntelligenceV21:


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

            (100-risk_score) * 0.25

            +

            pattern_score * 0.20

            +

            network_score * 0.10

            +

            market_strength * 0.05

        )



        # =========================
        # HISTORY
        # =========================


        if sample_size <= 1:

            evidence = "EARLY DATA"
            history_weight = 0.75


        elif sample_size <= 5:

            evidence = "LIMITED HISTORY"
            history_weight = 0.85


        elif sample_size <= 20:

            evidence = "GOOD HISTORY"
            history_weight = 0.95


        else:

            evidence = "STRONG HISTORY"
            history_weight = 1.0



        final_score = int(
            base_score * history_weight
        )



        # =========================
        # EARLY ALPHA OVERRIDE
        # =========================


        override = False


        if (

            alpha_score >= 70

            and risk_score <= 15

            and pattern_score >= 90

            and breakout

        ):

            override = True

            final_score = max(
                final_score,
                85
            )



        if survivor:

            final_score += 3



        final_score = min(
            100,
            final_score
        )



        # =========================
        # PROBABILITY
        # =========================


        alpha_probability = min(
            95,
            alpha_score + (
                15 if override else 0
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



        if override:

            alpha_type = "EARLY ALPHA"

        elif sample_size >=10 and alpha_score >=70:

            alpha_type = "PROVEN ALPHA"

        elif risk_score >=70:

            alpha_type = "RISK CREATOR"

        else:

            alpha_type = "UNKNOWN"



        signals=[]


        if breakout:

            signals.append(
                "Breakout token detected"
            )


        if survivor:

            signals.append(
                "Survival token detected"
            )


        if pattern_score >=90:

            signals.append(
                "Clean creator pattern"
            )


        if override:

            signals.append(
                "Early alpha override active"
            )


        if risk_score >=70:

            signals.append(
                "High risk creator"
            )



        return {

            "creator": creator,

            "final_score": final_score,

            "decision": decision,

            "alpha_type": alpha_type,

            "alpha_probability": alpha_probability,

            "rug_probability": rug_probability,

            "evidence": evidence,

            "sample_size": sample_size,

            "history_weight": history_weight,

            "override": override,

            "market_strength": market_strength,

            "pattern_score": pattern_score,

            "network_score": network_score,

            "signals": signals

        }




if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    )


    engine = CreatorIntelligenceV21()


    result = engine.analyze(
        creator
    )


    print()

    print("==============================")
    print(" CREATOR INTELLIGENCE V21 ")
    print("==============================")


    for key,value in result.items():

        print(
            f"{key:<22}: {value}"
        )