import sqlite3
import os

DB = os.path.join(
    "backend",
    "database",
    "tokens.db"
)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("PRAGMA table_info(tokens)")

for c in cur.fetchall():
    print(c)

conn.close()