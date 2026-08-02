import sqlite3



DB_PATH = "backend/database/tokens.db"



def create_table():


    conn = sqlite3.connect(
        DB_PATH
    )


    cursor = conn.cursor()



    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS creator_analysis (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            creator TEXT UNIQUE,

            final_score INTEGER,

            verdict TEXT,

            confidence TEXT,

            creator_score INTEGER,

            pattern_score INTEGER,

            behavior_score INTEGER,

            behavior_risk INTEGER,

            survival_score INTEGER,

            reasons TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )



    conn.commit()

    conn.close()



    print(
        "creator_analysis table created"
    )





if __name__ == "__main__":


    create_table()