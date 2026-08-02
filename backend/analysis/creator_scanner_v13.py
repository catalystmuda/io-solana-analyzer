from backend.analysis.creator_intelligence_v12 import CreatorIntelligenceV12

import sqlite3




class CreatorScannerV13:



    def __init__(self):


        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )


        self.cursor = self.conn.cursor()


        self.engine = CreatorIntelligenceV12()




    # =====================================
    # GET ALL CREATORS
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
    # SCAN ALL CREATOR
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

            key=lambda x:
            x["final_score"],

            reverse=True

        )


        return results





    # =====================================
    # CLOSE
    # =====================================


    def close(self):


        self.engine.close()

        self.conn.close()





# =====================================
# TEST
# =====================================


if __name__ == "__main__":



    scanner = CreatorScannerV13()



    results = scanner.scan()



    print()

    print("==============================")

    print(" CREATOR SCANNER V13 ")

    print("==============================")




    print()

    print("==============================")

    print(" ENTRY CANDIDATE ")

    print("==============================")



    count = 1



    for r in results:


        if r["decision"] == "ENTRY CANDIDATE":


            print()

            print(
                f"#{count}"
            )


            print(
                f"Creator      : {r['creator']}"
            )


            print(
                f"Score        : {r['final_score']}"
            )


            print(
                f"Success      : {r['success_probability']}%"
            )


            print(
                f"Risk         : {r['rug_probability']}%"
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
                f"Creator      : {r['creator']}"
            )


            print(
                f"Score        : {r['final_score']}"
            )


            print(
                f"Success      : {r['success_probability']}%"
            )


            count += 1






    print()

    print("==============================")

    print(" AVOID CREATOR ")

    print("==============================")



    count = 1



    for r in results:


        if r["decision"] == "AVOID":


            print()

            print(
                f"#{count}"
            )


            print(
                f"Creator      : {r['creator']}"
            )


            print(
                f"Score        : {r['final_score']}"
            )


            print(
                f"Risk         : {r['rug_probability']}%"
            )


            count += 1




    scanner.close()