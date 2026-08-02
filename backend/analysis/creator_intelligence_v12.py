from backend.analysis.creator_intelligence_v11 import CreatorIntelligenceV11
from backend.analysis.creator_probability import CreatorProbability



class CreatorIntelligenceV12:


    def __init__(self):

        self.v11 = CreatorIntelligenceV11()

        self.probability_engine = CreatorProbability()



    # =====================================
    # ANALYZE CREATOR V12
    # =====================================


    def analyze(self, creator):


        base = self.v11.analyze(
            creator
        )


        if not base:

            return None



        probability = self.probability_engine.calculate(
            base
        )



        final_score = round(

            (

                base["final_score"] * 0.70

                +

                probability["success_probability"] * 0.30

            )

        )



        if final_score >= 80:

            tier = "ALPHA CREATOR"


        elif final_score >= 65:

            tier = "EARLY PROMISING"


        elif final_score >= 50:

            tier = "WATCH LIST"


        elif final_score >= 35:

            tier = "HIGH RISK CREATOR"


        else:

            tier = "AVOID CREATOR"




        return {


            **base,


            "final_score": final_score,


            "tier": tier,


            "alpha_probability":
                probability["alpha_probability"],


            "rug_probability":
                probability["rug_probability"],


            "success_probability":
                probability["success_probability"],


            "decision":
                probability["decision"]

        }





    def close(self):

        self.v11.close()





# =====================================
# TEST
# =====================================


if __name__ == "__main__":



    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorIntelligenceV12()



    result = engine.analyze(
        creator
    )



    print()

    print("==============================")

    print(" CREATOR INTELLIGENCE V12 ")

    print("==============================")



    if result is None:


        print(
            "Creator tidak ditemukan"
        )


    else:


        print(
            f"Creator              : {result['creator']}"
        )


        print("--------------------------------")


        print(
            f"Final Score          : {result['final_score']}/100"
        )


        print(
            f"Tier                 : {result['tier']}"
        )


        print("--------------------------------")


        print(
            f"Alpha Probability    : {result['alpha_probability']}%"
        )


        print(
            f"Rug Probability      : {result['rug_probability']}%"
        )


        print(
            f"Success Probability  : {result['success_probability']}%"
        )


        print(
            f"Decision             : {result['decision']}"
        )


        print("--------------------------------")


        print("SIGNALS")


        for r in result["reasons"]:

            print(
                "-",
                r
            )



    engine.close()