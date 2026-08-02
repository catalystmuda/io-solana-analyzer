from backend.analysis.creator_intelligence_v6 import CreatorIntelligenceV6



class CreatorIntelligenceV7:


    def __init__(self):

        self.engine = CreatorIntelligenceV6()



    def analyze(self, creator):


        result = self.engine.analyze(
            creator
        )


        if not result:

            return None




        score = result["final_score"]



        survival = result.get(
            "survival_score",
            0
        )


        reliability = result.get(
            "reliability_score",
            0
        )



        reasons = result["reasons"][:]



        early_success = False




        # ==========================
        # EARLY SUCCESS DETECTION
        # ==========================


        if (
            result["history"] == "NEW CREATOR"
            and survival >= 80
        ):


            early_success = True


            score += 10


            reasons.append(
                "Early successful launch detected"
            )



        if reliability >= 60:


            score += 5


            reasons.append(
                "Creator reliability signal positive"
            )




        if score > 100:

            score = 100





        # ==========================
        # NEW TIER
        # ==========================


        if early_success and score >= 60:


            tier = "EARLY PROMISING"



        elif score >= 80:


            tier = "ALPHA CREATOR"



        elif score >= 60:


            tier = "PROMISING CREATOR"



        elif score >= 40:


            tier = "NEUTRAL CREATOR"



        else:


            tier = "HIGH RISK CREATOR"







        return {


            **result,


            "final_score": score,

            "tier_v7": tier,

            "early_success": early_success,

            "reasons": reasons


        }





    def close(self):

        self.engine.close()







# ==========================
# TEST
# ==========================


if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorIntelligenceV7()



    result = engine.analyze(
        creator
    )



    print()

    print("==============================")
    print(" CREATOR INTELLIGENCE V7 ")
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
            f"Tier           : {result['tier_v7']}"
        )


        print(
            f"Early Success  : {result['early_success']}"
        )


        print(
            f"Confidence     : {result['confidence_v6']}"
        )


        print(
            f"History        : {result['history']}"
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