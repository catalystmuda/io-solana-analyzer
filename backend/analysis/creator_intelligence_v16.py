from backend.analysis.creator_intelligence_v15 import CreatorIntelligenceV15


class CreatorIntelligenceV16:

    def __init__(self):

        self.engine = CreatorIntelligenceV15()


    def confidence_adjustment(
        self,
        result
    ):

        total_token = result.get(
            "total_token",
            0
        )

        score = result["final_score"]


        confidence = "LOW"

        if total_token >= 10:
            confidence = "MEDIUM"

        if total_token >= 30:
            confidence = "HIGH"


        # early alpha boost
        if (
            result.get("alpha_probability",0)
            >=70
            and score >=70
        ):
            if confidence == "LOW":
                confidence = "MEDIUM"


        return confidence



    def analyze(
        self,
        creator
    ):

        base = self.engine.analyze(
            creator
        )


        confidence = self.confidence_adjustment(
            base
        )


        total_token = base.get(
            "total_token",
            0
        )


        data_quality = "LIMITED"


        if total_token >=10:
            data_quality="GOOD"


        if total_token >=50:
            data_quality="STRONG"



        return {

            **base,

            "confidence":
                confidence,

            "data_quality":
                data_quality,

            "sample_size":
                total_token

        }



if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    )


    engine = CreatorIntelligenceV16()


    result = engine.analyze(
        creator
    )


    print()

    print("==============================")
    print(" CREATOR INTELLIGENCE V16 ")
    print("==============================")

    print(
        f"Creator          : {creator}"
    )

    print("--------------------------------")

    print(
        f"Final Score      : {result['final_score']}/100"
    )

    print(
        f"Decision         : {result['decision']}"
    )

    print("--------------------------------")

    print(
        f"Alpha Probability : {result['alpha_probability']}%"
    )

    print(
        f"Rug Probability   : {result['rug_probability']}%"
    )


    print("--------------------------------")

    print(
        f"Confidence       : {result['confidence']}"
    )

    print(
        f"Data Quality     : {result['data_quality']}"
    )

    print(
        f"Sample Size      : {result['sample_size']} token"
    )


    print("--------------------------------")

    print("SIGNALS")


    for s in result.get(
        "signals",
        []
    ):

        print(
            "-",
            s
        )