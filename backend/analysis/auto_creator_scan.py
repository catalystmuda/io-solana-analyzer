import sqlite3

from backend.analysis.creator_intelligence import CreatorIntelligence
from backend.analysis.save_creator_analysis import SaveCreatorAnalysis




class AutoCreatorScan:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()




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





    def run(self):


        creators = self.get_creators()


        print()

        print("==============================")
        print("AUTO CREATOR SCAN")
        print("==============================")

        print(
            "Total Creator :",
            len(creators)
        )


        intelligence = CreatorIntelligence()

        saver = SaveCreatorAnalysis()



        for i, creator in enumerate(creators, 1):


            print()

            print(
                f"[{i}/{len(creators)}] Analyzing"
            )


            print(
                creator
            )



            result = intelligence.analyze(
                creator
            )



            if result:


                saver.save(
                    result
                )


                print(
                    "Saved"
                )



        saver.close()

        intelligence.close()





        print()

        print(
            "SCAN COMPLETE"
        )





if __name__ == "__main__":


    engine = AutoCreatorScan()


    engine.run()

