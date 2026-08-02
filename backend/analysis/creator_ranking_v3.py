import sqlite3

from backend.analysis.creator_intelligence_v5 import CreatorIntelligenceV5



class CreatorRankingV3:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()

        self.engine = CreatorIntelligenceV5()



    # =====================================
    # GET CREATOR LIST
    # =====================================

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
            row[0]
            for row in rows
        ]



    # =====================================
    # SCAN ALL CREATOR
    # =====================================

    def scan(self):


        creators = self.get_creators()


        results = []


        print()

        print("==============================")
        print(" CREATOR RANKING V3 SCAN ")
        print("==============================")


        print(
            f"Total Creator : {len(creators)}"
        )



        for i, creator in enumerate(creators,1):


            try:

                data = self.engine.analyze(
                    creator
                )


                if data:

                    results.append(
                        data
                    )


                print(
                    f"[{i}/{len(creators)}] {creator[:8]}..."
                )


            except Exception as e:


                print(
                    "ERROR",
                    creator,
                    e
                )



        return results



    # =====================================
    # DISPLAY ALPHA
    # =====================================

    def show_alpha(self, results):


        results = sorted(

            results,

            key=lambda x:x["final_score"],

            reverse=True

        )



        print()

        print("==============================")
        print(" TOP ALPHA CREATOR V3 ")
        print("==============================")



        for index,item in enumerate(results[:10],1):


            print()

            print(
                f"#{index}"
            )

            print(
                f"Creator       : {item['creator']}"
            )

            print(
                f"AI Score      : {item['final_score']}"
            )

            print(
                f"Verdict       : {item['verdict']}"
            )

            print(
                f"Confidence    : {item['confidence']}"
            )

            print(
                f"Weight        : {item['confidence_weight']}"
            )

            print(
                f"Survival      : {item['survival_score']}"
            )

            print(
                f"Reliability   : {item['reliability_score']}"
            )



    # =====================================
    # DISPLAY RISK
    # =====================================

    def show_risk(self, results):


        results = sorted(

            results,

            key=lambda x:x["final_score"]

        )



        print()

        print("==============================")
        print(" HIGH RISK CREATOR V3 ")
        print("==============================")



        for index,item in enumerate(results[:10],1):


            print()

            print(
                f"#{index}"
            )

            print(
                f"Creator       : {item['creator']}"
            )


            print(
                f"AI Score      : {item['final_score']}"
            )


            print(
                f"Verdict       : {item['verdict']}"
            )


            print(
                f"Confidence    : {item['confidence']}"
            )


            print(
                f"Survival      : {item['survival_score']}"
            )


            print(
                "Reasons:"
            )


            for reason in item["reasons"]:

                print(
                    "-",
                    reason
                )



    def close(self):


        self.engine.close()

        self.conn.close()





# =====================================
# TEST
# =====================================


if __name__ == "__main__":


    ranking = CreatorRankingV3()


    data = ranking.scan()


    ranking.show_alpha(
        data
    )


    ranking.show_risk(
        data
    )


    ranking.close()