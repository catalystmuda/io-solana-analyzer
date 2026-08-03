import sqlite3
import os

DB = os.path.join(
    "backend",
    "database",
    "tokens.db"
)

conn = sqlite3.connect(DB)
cur = conn.cursor()

creator = input("Creator : ").strip()

cur.execute("""
SELECT
total_tokens,
highest_mc,
average_mc,
breakout_count,
survivor_count,
reputation_score,
risk_score,
category
FROM creator_memory
WHERE creator=?
""",(creator,))

row = cur.fetchone()

print("="*60)

if not row:
    print("Creator belum ada di memory.")
    exit()

print("TOTAL TOKEN :",row[0])
print("HIGHEST MC  :",round(row[1],2))
print("AVERAGE MC  :",round(row[2],2))
print("BREAKOUT    :",row[3])
print("SURVIVOR    :",row[4])
print("REPUTATION  :",row[5])
print("RISK        :",row[6])
print("CATEGORY    :",row[7])

print("="*60)

if row[7]=="ELITE":
    print("🔥 BUY EVERY LAUNCH")

elif row[7]=="GOOD":
    print("✅ PRIORITY WATCH")

elif row[7]=="NORMAL":
    print("👀 WATCH")

else:
    print("❌ SKIP")