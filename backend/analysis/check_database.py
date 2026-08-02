import sqlite3


DB = "backend/database/tokens.db"


def check_database():

    print("==============================")
    print(" DATABASE INSPECTOR ")
    print("==============================")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()


    print("\nTABLE LIST\n")

    cursor.execute("""
        SELECT name 
        FROM sqlite_master
        WHERE type='table'
    """)

    tables = cursor.fetchall()


    if not tables:
        print("NO TABLE FOUND")
        return


    for t in tables:
        print("-", t[0])


    print("\nCOLUMN CHECK\n")


    for table in tables:

        table_name = table[0]

        print("----------------")
        print("TABLE :", table_name)

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = cursor.fetchall()


        for col in columns:
            print(
                col[1],
                "| TYPE:",
                col[2]
            )


    conn.close()



if __name__ == "__main__":
    check_database()