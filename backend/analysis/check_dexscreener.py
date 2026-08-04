import sqlite3
import requests
import json

conn = sqlite3.connect("backend/database/tokens.db")
conn.row_factory = sqlite3.Row

row = conn.execute("""
SELECT *
FROM tokens
ORDER BY market_cap_sol DESC
LIMIT 1
""").fetchone()

mint = row["mint"]

print("="*70)
print("TOKEN")
print("="*70)
print(row["name"])
print(mint)
print()

url = f"https://api.dexscreener.com/latest/dex/tokens/{mint}"

r = requests.get(url, timeout=20)

print("STATUS :", r.status_code)
print()

if r.status_code == 200:
    print(json.dumps(r.json(), indent=4))
else:
    print(r.text)

conn.close()