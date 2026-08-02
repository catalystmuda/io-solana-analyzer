from backend.analysis.creator_intelligence_v12 import CreatorIntelligenceV12
from backend.analysis.creator_calibration_v2 import CreatorCalibrationV2
from backend.analysis.creator_pattern_memory import CreatorPatternMemory
from backend.analysis.creator_network import CreatorNetwork





class CreatorIntelligenceV15:



    def __init__(self):


        self.probability = CreatorIntelligenceV12()

        self.calibration = CreatorCalibrationV2()

        self.pattern = CreatorPatternMemory()

        self.network = CreatorNetwork()






    # =====================================
    # FINAL CREATOR ANALYSIS
    # =====================================


    def analyze(self, creator):


        intelligence = self.probability.analyze(
            creator
        )


        calibration = self.calibration.analyze(
            creator
        )


        pattern = self.pattern.analyze(
            creator
        )


        network = self.network.analyze(
            creator
        )



        if not intelligence:

            return None






        # ==============================
        # COMPONENT
        # ==============================


        alpha = intelligence.get(
            "alpha_probability",
            0
        )


        success = intelligence.get(
            "success_probability",
            0
        )


        risk = intelligence.get(
            "rug_probability",
            100
        )



        calibration_score = calibration.get(
            "calibration_score",
            0
        )



        pattern_score = pattern.get(
            "pattern_score",
            0
        )



        network_score = network.get(
            "network_score",
            0
        )







        # ==============================
        # FINAL SCORE
        # ==============================


        final_score = round(


            alpha * 0.30

            +

            success * 0.20

            +

            calibration_score * 0.25

            +

            pattern_score * 0.15

            +

            network_score * 0.10


        )




        # Risk penalty


        final_score -= round(
            risk * 0.15
        )



        final_score = max(
            0,
            min(
                final_score,
                100
            )
        )







        # ==============================
        # DECISION
        # ==============================


        if final_score >= 75:


            decision = "ENTRY CANDIDATE"



        elif final_score >= 50:


            decision = "WATCH LIST"



        else:


            decision = "AVOID"







        reasons = []




        if alpha >= 60:


            reasons.append(
                "Alpha signal detected"
            )



        if success >= 60:


            reasons.append(
                "Success probability strong"
            )



        if risk >= 70:


            reasons.append(
                "High rug probability"
            )



        if calibration_score >= 60:


            reasons.append(
                "Strong creator calibration"
            )



        if pattern_score >= 80:


            reasons.append(
                "Clean creator pattern"
            )


        elif pattern_score < 40:


            reasons.append(
                "Dangerous creator pattern"
            )



        return {


            "creator": creator,

            "final_score": final_score,

            "decision": decision,


            "alpha_probability": alpha,

            "success_probability": success,

            "rug_probability": risk,


            "calibration": calibration_score,

            "pattern": pattern_score,

            "network": network_score,


            "reasons": reasons

        }





    def close(self):


        self.probability.close()

        self.calibration.close()

        self.pattern.close()

        self.network.close()






# =====================================
# TEST
# =====================================


if __name__ == "__main__":



    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorIntelligenceV15()



    result = engine.analyze(
        creator
    )



    print()


    print("==============================")

    print(" CREATOR INTELLIGENCE V15 ")

    print("==============================")



    if result is None:


        print(
            "Creator tidak ditemukan"
        )


    else:



        print(
            f"Creator             : {result['creator']}"
        )


        print("--------------------------------")



        print(
            f"Final Score         : {result['final_score']}/100"
        )


        print(
            f"Decision            : {result['decision']}"
        )


        print("--------------------------------")



        print(
            f"Alpha Probability   : {result['alpha_probability']}%"
        )


        print(
            f"Success Probability : {result['success_probability']}%"
        )


        print(
            f"Rug Probability     : {result['rug_probability']}%"
        )


        print("--------------------------------")



        print(
            f"Calibration         : {result['calibration']}"
        )


        print(
            f"Pattern             : {result['pattern']}"
        )


        print(
            f"Network             : {result['network']}"
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