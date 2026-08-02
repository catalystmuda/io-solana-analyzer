import math



class CreatorProbability:



    # =====================================
    # CREATOR PROBABILITY ENGINE
    # =====================================


    def __init__(self):

        pass




    def calculate(self, data):


        alpha = data.get(
            "alpha_score",
            0
        )


        risk = data.get(
            "risk_score",
            100
        )


        reliability = data.get(
            "reliability",
            0
        )


        network = data.get(
            "network",
            0
        )


        temporal = data.get(
            "temporal",
            0
        )



        # =================================
        # ALPHA PROBABILITY
        # =================================


        alpha_probability = (

            alpha * 0.45

            +

            reliability * 0.20

            +

            network * 0.15

            +

            temporal * 0.20

        )



        alpha_probability = round(
            min(alpha_probability,100)
        )



        # =================================
        # RUG PROBABILITY
        # =================================


        rug_probability = (

            risk * 0.50

            +

            (100 - reliability) * 0.20

            +

            (100 - temporal) * 0.20

            +

            (100 - network) * 0.10

        )



        rug_probability = round(

            min(rug_probability,100)

        )



        # =================================
        # SUCCESS PROBABILITY
        # =================================


        success_probability = round(

            (

                alpha_probability

                +

                (100-rug_probability)

            )

            / 2

        )




        # =================================
        # DECISION
        # =================================


        if success_probability >= 75:

            decision = "ENTRY CANDIDATE"


        elif success_probability >= 50:

            decision = "WATCH LIST"


        else:

            decision = "AVOID"




        return {



            "alpha_probability":
                alpha_probability,


            "rug_probability":
                rug_probability,


            "success_probability":
                success_probability,


            "decision":
                decision

        }



    def close(self):

        pass