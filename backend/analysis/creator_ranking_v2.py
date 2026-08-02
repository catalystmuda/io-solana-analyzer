import sqlite3

from backend.analysis.creator_intelligence_v4 import CreatorIntelligenceV4



class CreatorRankingV2:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()

        self.engine = CreatorIntelligenceV4()



    # =====================================
    # AMBIL SEMUA CREATOR
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
            r[0]
            for r in rows
        ]



    # =====================================
    # RANKING CREATOR
    # =====================================

    def ranking(self):


        creators = self.get_creators()


        results = []



        print()

        print("==============================")
        print("CREATOR RANKING V2 SCAN")
        print("==============================")

        print(
            f"Total Creator : {len(creators)}"
        )



        for index, creator in enumerate(creators,1):


            try:

                result = self.engine.analyze(
                    creator
                )


                if result:

                    results.append(
                        result
                    )


                print(
                    f"[{index}/{len(creators)}] analyzed"
                )


            except Exception as e:


                print(
                    "ERROR:",
                    creator,
                    e
                )



        return results




    # =====================================
    # DISPLAY
    # =====================================

    def show(self, results):


        results = sorted(
            results,
            key=lambda x:x["final_score"],
            reverse=True
        )


        print()

        print("==============================")
        print(" TOP ALPHA CREATOR V2 ")
        print("==============================")



        for i,item in enumerate(results[:10],1):


            print()

            print(
                f"#{i}"
            )

            print(
                f"Creator      : {item['creator']}"
            )

            print(
                f"Score        : {item['final_score']}"
            )

            print(
                f"Verdict      : {item['verdict']}"
            )

            print(
                f"Confidence   : {item['confidence']}"
            )

            print(
                f"Survival     : {item['survival_score']}"
            )

            print(
                f"Reliability  : {item['reliability_score']}"
            )



        print()

        print("==============================")
        print(" HIGH RISK CREATOR V2 ")
        print("==============================")



        risky = sorted(
            results,
            key=lambda x:x["final_score"]
        )



        for i,item in enumerate(risky[:10],1):


            print()

            print(
                f"#{i}"
            )


            print(
                f"Creator      : {item['creator']}"
            )

            print(
                f"Score        : {item['final_score']}"
            )

            print(
                f"Verdict      : {item['verdict']}"
            )

            print(
                f"Behavior Risk: {item['behavior_risk']}"
            )

            print(
                f"Survival     : {item['survival_score']}"
            )



            print(
                "Reasons:"
            )


            for r in item["reasons"]:

                print(
                    "-",
                    r
                )



    def close(self):

        self.engine.close()

        self.conn.close()





# =====================================
# TEST
# =====================================


if __name__ == "__main__":


    ranking = CreatorRankingV2()


    results = ranking.ranking()


    ranking.show(
        results
    )


    ranking.close()