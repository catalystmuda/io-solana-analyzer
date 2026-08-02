import sqlite3

conn = sqlite3.connect(
    "backend/database/tokens.db"
)

cursor = conn.cursor()

cursor.execute(
    "PRAGMA table_info(tokens)"
)

rows = cursor.fetchall()

print()
print("==============================")
print("TOKENS TABLE SCHEMA")
print("==============================")

for row in rows:
    print(row)

conn.close()