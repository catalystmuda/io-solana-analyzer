from backend.analysis.creator_intelligence_v5 import CreatorIntelligenceV5


class CreatorIntelligenceV6:


    def __init__(self):

        self.engine = CreatorIntelligenceV5()



    def analyze(self, creator):


        result = self.engine.analyze(
            creator
        )


        if not result:
            return None



        score = result["final_score"]


        total_token = 0


        try:

            total_token = (
                result.get(
                    "total_token",
                    0
                )
            )

        except:

            total_token = 0




        # ============================
        # HISTORY CLASS
        # ============================


        if total_token <= 2:

            history = "NEW CREATOR"


        elif total_token < 20:

            history = "GROWING CREATOR"


        else:

            history = "EXPERIENCED CREATOR"




        # ============================
        # CONFIDENCE
        # ============================


        if total_token < 3:

            confidence = "LOW"


        elif total_token < 20:

            confidence = "MEDIUM"


        else:

            confidence = "HIGH"





        # ============================
        # DATA QUALITY
        # ============================


        if total_token < 3:

            quality = "LIMITED"


        elif total_token < 20:

            quality = "GOOD"


        else:

            quality = "STRONG"






        # ============================
        # CREATOR TIER
        # ============================


        if score >= 80:


            tier = "ALPHA CREATOR"


        elif score >= 60:


            if total_token < 3:

                tier = "EARLY PROMISING"


            else:

                tier = "PROMISING CREATOR"



        elif score >= 40:


            tier = "NEUTRAL CREATOR"


        else:


            tier = "HIGH RISK CREATOR"






        reasons = result["reasons"][:]



        if total_token < 3:

            reasons.append(
                "Limited creator history"
            )



        return {


            **result,


            "tier": tier,

            "history": history,

            "confidence_v6": confidence,

            "data_quality": quality,

            "reasons": reasons


        }



    def close(self):

        self.engine.close()







# ===============================
# TEST
# ===============================


if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorIntelligenceV6()



    result = engine.analyze(
        creator
    )



    print()


    print("==============================")
    print(" CREATOR INTELLIGENCE V6 ")
    print("==============================")



    if result:


        print(
            f"Creator        : {result['creator']}"
        )


        print("--------------------------------")


        print(
            f"AI Score       : {result['final_score']}"
        )


        print(
            f"Tier           : {result['tier']}"
        )


        print(
            f"Confidence     : {result['confidence_v6']}"
        )


        print(
            f"History        : {result['history']}"
        )


        print(
            f"Data Quality   : {result['data_quality']}"
        )


        print("--------------------------------")


        print("REASONS")


        for r in result["reasons"]:

            print(
                "-",
                r
            )


    else:


        print(
            "Creator tidak ditemukan"
        )



    engine.close()