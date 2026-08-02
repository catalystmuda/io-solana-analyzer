from backend.analysis.creator_intelligence_v12 import CreatorIntelligenceV12

import sqlite3




class CreatorScannerV14:


    def __init__(self):


        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )


        self.cursor = self.conn.cursor()


        self.engine = CreatorIntelligenceV12()




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
            x[0]
            for x in rows
        ]





    # =====================================
    # HUNTER SCORE
    # =====================================


    def calculate_hunter_score(
            self,
            data
    ):


        score = (

            data["final_score"] * 0.40

            +

            data["alpha_probability"] * 0.25

            +

            data["success_probability"] * 0.25

            +

            data.get(
                "reliability_score",
                50
            ) * 0.10

        )


        return round(score)





    # =====================================
    # SCAN
    # =====================================


    def scan(self):


        creators = self.get_creators()


        results = []



        for creator in creators:


            try:


                result = self.engine.analyze(
                    creator
                )


                if result:


                    result["hunter_score"] = self.calculate_hunter_score(
                        result
                    )


                    results.append(
                        result
                    )


            except Exception as e:


                print(
                    "ERROR",
                    creator,
                    e
                )




        results.sort(

            key=lambda x:
            x["hunter_score"],

            reverse=True

        )


        return results






    def close(self):


        self.engine.close()

        self.conn.close()





# =====================================
# DISPLAY
# =====================================


if __name__ == "__main__":


    scanner = CreatorScannerV14()


    results = scanner.scan()



    print()

    print("==============================")

    print(" CREATOR SCANNER V14 ")

    print("==============================")





    print()

    print("==============================")

    print(" TOP ALPHA HUNTER ")

    print("==============================")



    count = 1



    for r in results[:20]:


        if r["decision"] == "ENTRY CANDIDATE":


            print()

            print(
                f"#{count}"
            )


            print(
                f"Creator       : {r['creator']}"
            )


            print(
                f"Hunter Score  : {r['hunter_score']}"
            )


            print(
                f"Alpha         : {r['alpha_probability']}%"
            )


            print(
                f"Success       : {r['success_probability']}%"
            )


            print(
                f"Risk          : {r['rug_probability']}%"
            )


            count += 1





    print()

    print("==============================")

    print(" WATCH LIST ")

    print("==============================")



    count = 1



    for r in results:


        if r["decision"] == "WATCH LIST":


            print()

            print(
                f"#{count}"
            )


            print(
                f"Creator       : {r['creator']}"
            )


            print(
                f"Hunter Score  : {r['hunter_score']}"
            )


            count += 1


            if count > 20:

                break





    print()

    print("==============================")

    print(" DANGER CREATOR ")

    print("==============================")



    count = 1



    for r in results:


        if r["decision"] == "AVOID":


            print()

            print(
                f"#{count}"
            )


            print(
                f"Creator       : {r['creator']}"
            )


            print(
                f"Hunter Score  : {r['hunter_score']}"
            )


            print(
                f"Risk          : {r['rug_probability']}%"
            )


            count += 1


            if count > 20:

                break




    scanner.close()