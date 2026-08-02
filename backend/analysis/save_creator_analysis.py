import sqlite3
import json

from backend.analysis.creator_intelligence import CreatorIntelligence



class SaveCreatorAnalysis:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()



    # ======================================
    # SAVE ANALYSIS RESULT
    # ======================================


    def save(self, result):


        self.cursor.execute(
            """
            INSERT OR REPLACE INTO creator_analysis (

                creator,

                final_score,

                verdict,

                confidence,

                creator_score,

                pattern_score,

                behavior_score,

                behavior_risk,

                survival_score,

                reasons

            )

            VALUES (?,?,?,?,?,?,?,?,?,?)

            """,

            (

                result["creator"],

                result["final_score"],

                result["verdict"],

                result["confidence"],

                result["creator_score"],

                result["pattern_score"],

                result["behavior_score"],

                result["behavior_risk"],

                result["survival_score"],

                json.dumps(
                    result["reasons"]
                )

            )

        )


        self.conn.commit()



        print(
            "Analysis saved successfully"
        )




    def close(self):

        self.conn.close()







# ==========================================
# TEST SAVE
# ==========================================


if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    intelligence = CreatorIntelligence()



    result = intelligence.analyze(
        creator
    )



    if result is None:


        print(
            "Creator tidak ditemukan"
        )



    else:


        saver = SaveCreatorAnalysis()


        saver.save(
            result
        )


        saver.close()



    intelligence.close()