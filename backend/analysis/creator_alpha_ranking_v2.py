from backend.analysis.creator_intelligence_v10 import CreatorIntelligenceV10
import sqlite3



class CreatorAlphaRankingV2:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()

        self.engine = CreatorIntelligenceV10()



    # ==========================================
    # GET ALL CREATOR
    # ==========================================


    def get_creators(self):


        self.cursor.execute(
            """
            SELECT DISTINCT creator
            FROM tokens
            WHERE creator IS NOT NULL
            """
        )


        rows = self.cursor.fetchall()


        return [

            r[0]

            for r in rows

        ]





    # ==========================================
    # RUN RANKING
    # ==========================================


    def ranking(self):


        creators = self.get_creators()



        results = []



        total = len(creators)



        print()

        print("==============================")

        print(
            "CREATOR ALPHA RANKING V2"
        )

        print("==============================")

        print(
            f"Total Creator : {total}"
        )

        print()



        for index, creator in enumerate(creators,1):


            print(
                f"[{index}/{total}] Analyzing {creator}"
            )



            try:


                result = self.engine.analyze(
                    creator
                )



                if result:


                    results.append(
                        result
                    )



            except Exception as e:


                print(
                    "ERROR:",
                    creator,
                    e
                )





        results.sort(

            key=lambda x: x["final_score"],

            reverse=True

        )


        return results





    # ==========================================
    # DISPLAY
    # ==========================================


    def display(self, results):


        alpha = []

        promising = []

        watch = []

        avoid = []




        for r in results:


            if r["tier"] == "ALPHA CREATOR":

                alpha.append(r)


            elif r["tier"] == "EARLY PROMISING":

                promising.append(r)


            elif r["tier"] == "WATCH LIST":

                watch.append(r)


            else:

                avoid.append(r)





        print()

        print("==============================")

        print(" TOP ALPHA CREATOR ")

        print("==============================")



        for i,r in enumerate(alpha[:10],1):


            self.print_creator(
                i,
                r
            )





        print()

        print("==============================")

        print(" EARLY PROMISING CREATOR ")

        print("==============================")



        for i,r in enumerate(promising[:10],1):


            self.print_creator(
                i,
                r
            )





        print()

        print("==============================")

        print(" WATCH LIST ")

        print("==============================")



        for i,r in enumerate(watch[:10],1):


            self.print_creator(
                i,
                r
            )





        print()

        print("==============================")

        print(" AVOID CREATOR ")

        print("==============================")



        for i,r in enumerate(avoid[:10],1):


            print()

            print(
                f"#{i}"
            )


            print(
                f"Creator     : {r['creator']}"
            )


            print(
                f"Score       : {r['final_score']}"
            )


            print(
                f"Risk        : {r['risk_score']}"
            )


            print(
                f"Risk Level  : {r['risk_level']}"
            )



    # ==========================================
    # PRINT CREATOR
    # ==========================================


    def print_creator(self,index,r):


        print()

        print(
            f"#{index}"
        )


        print(
            f"Creator      : {r['creator']}"
        )


        print(
            f"Score        : {r['final_score']}"
        )


        print(
            f"Tier         : {r['tier']}"
        )


        print(
            f"Confidence   : {r['confidence']}"
        )


        print(
            f"Alpha        : {r['alpha_score']}"
        )


        print(
            f"Risk         : {r['risk_score']}"
        )


        print(
            f"Reliability  : {r['reliability_score']}"
        )


        print(
            f"Network      : {r['network_score']}"
        )





    def close(self):


        self.engine.close()

        self.conn.close()





# ==========================================
# TEST
# ==========================================


if __name__ == "__main__":



    ranking = CreatorAlphaRankingV2()



    results = ranking.ranking()



    ranking.display(
        results
    )



    ranking.close()