import sqlite3

conn = sqlite3.connect("backend/database/tokens.db")
conn.row_factory = sqlite3.Row

rows = conn.execute("""
SELECT *
FROM paper_trades
ORDER BY id DESC
""").fetchall()

print("=" * 80)
print("PAPER TRADES")
print("=" * 80)

for r in rows:
    print()
    print("TIME   :", r["created_at"])
    print("NAME   :", r["name"])
    print("SYMBOL :", r["symbol"])
    print("MC     :", round(r["market_cap"], 2))
    print("BUY    :", round(r["buy_sol"], 2))
    print("ALPHA  :", round(r["alpha_score"], 2))
    print("STATUS :", r["status"])

conn.close()