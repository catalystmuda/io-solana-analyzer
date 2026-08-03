import sqlite3
import os

DB_PATH = os.path.join(
    "backend",
    "database",
    "tokens.db"
)


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


cursor.execute("""
SELECT
id,
highest_mc,
breakout_count,
survivor_count
FROM creator_memory
""")

rows = cursor.fetchall()


for row in rows:

    row_id = row[0]
    highest_mc = row[1] or 0
    breakout = row[2] or 0
    survivor = row[3] or 0

    reputation = 0

    reputation += breakout * 20
    reputation += survivor * 5

    if highest_mc >= 50:
        reputation += 10

    if highest_mc >= 100:
        reputation += 20

    if highest_mc >= 300:
        reputation += 20

    if highest_mc >= 1000:
        reputation += 30

    reputation = min(reputation, 100)

    risk = max(0, 100 - reputation)

    if reputation >= 80:
        category = "ELITE"

    elif reputation >= 60:
        category = "GOOD"

    elif reputation >= 40:
        category = "NORMAL"

    else:
        category = "RISK"

    cursor.execute("""
    UPDATE creator_memory
    SET
        reputation_score=?,
        risk_score=?,
        category=?
    WHERE id=?
    """, (
        reputation,
        risk,
        category,
        row_id
    ))


conn.commit()
conn.close()

print("======================")
print("CREATOR SCORE FIX DONE")
print("======================")