import os
import sqlite3

print("=" * 60)

for root, dirs, files in os.walk("."):

    for file in files:

        if not file.endswith(".db"):
            continue

        path = os.path.join(root, file)

        try:
            conn = sqlite3.connect(path)

            tables = conn.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """).fetchall()

            conn.close()

            print(path)

            for t in tables:
                print("   ", t[0])

            print("-" * 40)

        except:
            pass