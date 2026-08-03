import sqlite3

DB = "backend/database/tokens.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

rows = cur.execute("""
SELECT
creator,
total_tokens,
highest_mc,
average_mc,
breakout_count,
survivor_count,
reputation_score,
risk_score,
category
FROM creator_memory
ORDER BY reputation_score DESC
LIMIT 30
""").fetchall()

print("==============================")
print(" BEST CREATOR MEMORY ")
print("==============================")

for i, row in enumerate(rows, 1):

    print()
    print(f"#{i}")
    print("-----------------------")
    print("Creator      :", row[0])
    print("Total Token  :", row[1])
    print("Highest MC   :", round(row[2], 2))
    print("Average MC   :", round(row[3], 2))
    print("Breakout     :", row[4])
    print("Survivor     :", row[5])
    print("Reputation   :", row[6])
    print("Risk         :", row[7])
    print("Category     :", row[8])

conn.close()