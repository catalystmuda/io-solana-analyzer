import sqlite3
import requests
import json

conn = sqlite3.connect("backend/database/tokens.db")
conn.row_factory = sqlite3.Row

row = conn.execute("""
SELECT mint,name,symbol
FROM tokens
ORDER BY market_cap_sol DESC
LIMIT 1
""").fetchone()

mint = row["mint"]

print("="*70)
print("TOKEN")
print("="*70)
print("NAME   :", row["name"])
print("SYMBOL :", row["symbol"])
print("MINT   :", mint)
print()

url = f"https://frontend-api-v3.pump.fun/coins/{mint}"

r = requests.get(url, timeout=15)

print("="*70)
print("STATUS :", r.status_code)
print("="*70)

if r.status_code == 200:
    data = r.json()
    print(json.dumps(data, indent=4))
else:
    print(r.text)

conn.close()