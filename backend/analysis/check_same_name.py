import sqlite3
from collections import defaultdict

conn = sqlite3.connect("backend/database/tokens.db")
conn.row_factory = sqlite3.Row

rows = conn.execute("""
SELECT name,symbol,creator,market_cap_sol,mint
FROM tokens
ORDER BY market_cap_sol DESC
""").fetchall()

groups = defaultdict(list)

for r in rows:

    name = (r["name"] or "").strip().lower()
    symbol = (r["symbol"] or "").strip().lower()

    if name == "" and symbol == "":
        continue

    key = (name, symbol)
    groups[key].append(r)

for key, items in groups.items():

    creators = set(x["creator"] for x in items)

    if len(creators) <= 1:
        continue

    print("=" * 70)
    print("NAME   :", items[0]["name"])
    print("SYMBOL :", items[0]["symbol"])

    for x in items:
        print(
            "MC:",
            round(x["market_cap_sol"],2),
            "|",
            x["creator"],
            "|",
            x["mint"]
        )

conn.close()